from sqlalchemy.orm import joinedload

from app.models.cards import Card, Category, db


def get_categories():
    return [c.value for c in db.session.query(Category.value).distinct().all()]


def get_show_cards(order_by):
    return (
        db.session.query(Card)
        .options(
            joinedload(Card.elements_list),
            joinedload(Card.job_list),
            joinedload(Card.categories_list),
            joinedload(Card.abilities_list),
        )
        .order_by(*order_by)
    )


def get_card_detail(card_id):
    return (
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
