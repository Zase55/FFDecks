from app.routes.auth import bp_auth
from app.routes.card_finder import bp_card_finder
from app.routes.deck_editor import bp_deck_editor
from app.routes.decks import bp_decks
from app.routes.formats import bp_formats
from app.routes.profile import bp_profile
from app.routes.submit_tournament import bp_submit_tournament
from app.routes.tournaments import bp_tournaments

blueprints = [
    {"bp": bp_auth, "url_prefix": "/auth"},
    {"bp": bp_profile, "url_prefix": "/profile"},
    {"bp": bp_card_finder, "url_prefix": "/card_finder"},
    {"bp": bp_decks, "url_prefix": "/decks"},
    {"bp": bp_deck_editor, "url_prefix": "/deck_editor"},
    {"bp": bp_tournaments, "url_prefix": "/tournaments"},
    {"bp": bp_submit_tournament, "url_prefix": "/submit_tournament"},
    {"bp": bp_formats, "url_prefix": "/formats"},
]
