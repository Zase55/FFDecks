import json
import os

import pandas as pd
from flask import Blueprint, render_template, request
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from app.models.cards import Ability, Card, Category, Element, Job, db
from app.routes.constants import menu_items

bp_cards = Blueprint("cards", __name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_dir, "..", "data", "scraping_result.xlsx")


@bp_cards.route("/", methods=["GET", "POST"])
def show_cards():
    limit = request.args.get("limit", 24)
    page = request.args.get("page", 1)
    order_asc = request.args.get("order_asc", True)

    if not isinstance(limit, int):
        limit = 24 if not limit.strip().isdigit() else int(limit)

    if not isinstance(page, int):
        page = 1 if not page.strip().isdigit() else int(page)

    offset = limit * (page - 1)

    if not isinstance(order_asc, bool):
        if order_asc.strip().lower() in ["true", "false"]:
            if order_asc.strip().lower() == "true":
                order_asc = [Card.collection, Card.serial]
            else:
                order_asc = [desc(Card.collection), desc(Card.serial)]
        else:
            order_asc = [Card.collection, Card.serial]
    else:
        order_asc = [Card.collection, Card.serial]

    cards = (
        db.session.query(Card)
        .options(
            joinedload(Card.elements_list),
            joinedload(Card.job_list),
            joinedload(Card.categories_list),
            joinedload(Card.abilities_list),
        )
        .order_by(*order_asc)
        .limit(limit)
        .offset(offset)
        .all()
    )
    return render_template("cards.html", cards=cards, menu=menu_items, title="Buscador")


@bp_cards.route("/<int:card_id>", methods=["GET", "POST"])
def card_detail(card_id):
    card = (
        db.session.query(Card)
        .options(
            joinedload(Card.elements_list),
            joinedload(Card.job_list),
            joinedload(Card.categories_list),
            joinedload(Card.abilities_list),
        )
        .filter_by(id=card_id)
        .first_or_404()
    )

    return render_template("card_detail.html", card=card, menu=menu_items)


@bp_cards.cli.command("populate")
def populate():
    df = pd.read_excel(excel_path)
    for _, row in df.iterrows():
        collection, serial = row["Number"].split("-") if pd.notna(row["Number"]) else (None, None)

        new_card = Card(
            name=row["Name"],
            number=row["Number"],
            image=row["Image"],
            rarity=row["Rarity"],
            card_set=row["Set"],
            cost=row["Cost"],
            card_type=row["Type"],
            exburst=row["Ex Burst"],
            multiplayable=row["Multiplayable"],
            power=row["Power"] if not pd.isna(row["Power"]) else None,
            collection=int(collection) if collection.isdigit() else collection,
            serial=serial,
        )

        db.session.add(new_card)
        db.session.commit()

        elements = json.loads(row["Element"])
        for order, element_value in enumerate(elements):
            element = Element(card_id=new_card.id, order=order + 1, value=element_value)
            db.session.add(element)

        jobs = json.loads(row["Job"])
        for order, job_value in enumerate(jobs):
            job = Job(card_id=new_card.id, order=order + 1, value=job_value)
            db.session.add(job)

        categories = json.loads(row["Categories"])
        for order, category_value in enumerate(categories):
            category = Category(card_id=new_card.id, order=order + 1, value=category_value)
            db.session.add(category)

        abilities = json.loads(row["Abilities"])  # Convertir el string JSON a lista de listas
        for row_idx, ability_row in enumerate(abilities):
            for col_idx, ability in enumerate(ability_row):
                for key, value in ability.items():
                    ability_entry = Ability(
                        card_id=new_card.id,
                        row=row_idx + 1,
                        column=col_idx + 1,
                        value_type=key,
                        value=value,
                    )
                    db.session.add(ability_entry)

                    if isinstance(value, str) and "limit break" in value.lower():
                        new_card.limit_break = "Yes"
                        db.session.add(new_card)

        db.session.commit()
    print("Datos cargados exitosamente.")
