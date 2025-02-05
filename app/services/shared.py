from flask import request
from sqlalchemy import desc


def get_pagination(query, page, limit):
    total = query.count()
    pages = max(1, (total // limit) + (1 if total % limit else 0))
    return {
        "page": page,
        "pages": pages,
        "has_prev": page > 1,
        "has_next": page < pages,
        "has_first": 1,
        "has_last": pages,
    }


def parse_request_args(*attributes):
    args = request.args.to_dict()
    limit = request.args.get("limit", 24, type=int)
    page = request.args.get("page", 1, type=int)
    order_asc = request.args.get("order_asc", "true").lower() == "true"
    order_by = [*attributes] if order_asc else [desc(attr) for attr in attributes]
    return args, limit, page, order_by
