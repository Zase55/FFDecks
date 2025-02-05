import json
import os
import urllib.parse

import pandas as pd
from flask import Blueprint, render_template, request
from sqlalchemy.orm import joinedload

from app.models.cards import Ability, Card, Category, Element, Job, db
from app.routes.constants import menu_items
from app.services.cards import get_card_detail, get_categories
from app.services.shared import get_pagination, parse_request_args

bp_cards = Blueprint("cards", __name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_dir, "..", "data", "scraping_result.xlsx")


@bp_cards.route("/<int:card_id>", methods=["GET"])
def card_detail(card_id):
    card = get_card_detail(card_id)
    return render_template("card_detail.html", card=card, menu=menu_items)


@bp_cards.route("/", methods=["GET"])
def show_cards():
    args, limit, page, order_by = parse_request_args(Card.collection, Card.serial)
    offset = limit * (page - 1)

    query = Card.query

    name = request.args.get("name")
    if name:
        query = query.filter(Card.name.ilike(f"%{name}%"))

    element = request.args.getlist("element")
    if element:
        query = query.join(Element).filter(Element.value.in_(element))

    card_type = request.args.getlist("card_type")
    if card_type:
        query = query.filter(Card.card_type.in_(card_type))

    cost = request.args.getlist("cost", type=int)
    if cost:
        query = query.filter(Card.cost.in_(cost))

    category_filter = request.args.get("category")
    if category_filter:
        query = query.join(Category).filter(Category.value == category_filter)

    operador = request.args.get("operator-power")
    power = request.args.get("power", type=int)
    if power:
        if operador == "=":
            query = query.filter(Card.power == power)
        elif operador == ">=":
            query = query.filter(Card.power >= power)
        elif operador == ">":
            query = query.filter(Card.power > power)
        elif operador == "<=":
            query = query.filter(Card.power <= power)
        elif operador == "<":
            query = query.filter(Card.power < power)

    rarity = request.args.get("rarity")
    if rarity:
        query = query.filter_by(rarity=rarity)

    job = request.args.get("job")
    if job:
        query = query.join(Job).filter(Job.value == job)

    ability_text = request.args.get("ability")
    if ability_text:
        query = query.join(Ability).filter(Ability.value.ilike(f"%{ability_text}%"))

    query = query.options(
        joinedload(Card.elements_list),
        joinedload(Card.job_list),
        joinedload(Card.categories_list),
        joinedload(Card.abilities_list),
    ).order_by(*order_by)

    pagination = get_pagination(query, page, limit)
    cards = query.limit(limit).offset(offset).all()
    args.setdefault("limit", request.args.get("limit", "24"))
    json_args = urllib.parse.urlencode(args)
    return render_template(
        "cards.html",
        cards=cards,
        args=json_args,
        menu=menu_items,
        title="Buscador",
        pagination=pagination,
        categories=get_categories(),
    )


@bp_cards.cli.command("populate")
def populate():
    df = pd.read_excel(excel_path)
    for _, row in df.iterrows():
        collection, serial = row["Number"].split("-") if pd.notna(row["Number"]) else (None, None)

        try:
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

            abilities = json.loads(row["Abilities"])
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

            db.session.commit()

        except Exception:
            continue
    print("Datos cargados exitosamente.")
