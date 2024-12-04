menu_items = [
    {"name": "Inicio", "url": "/"},
    {"name": "Buscador", "url": "/cards"},
    {"name": "Decks", "url": "/decks"},
    {"name": "Editor", "url": "/deck_editor"},
    {"name": "Torneos", "url": "/tournaments"},
    {"name": "Crear Torneo", "url": "/submit_tournament"},
    {"name": "Formatos", "url": "/formats"},
    {"name": "Login", "url": "/auth/login"},
    {"name": "Registrarse", "url": "/auth/register"},
]

menu_items_login = [
    {"name": "Inicio", "url": "/"},
    {
        "name": "Perfil",
        "url": "#",
        "submenu": [
            {"name": "Decks", "url": "/profile/my_decks"},
            {"name": "Torneos", "url": "/profile/my_tournaments"},
            {"name": "Mis Cartas", "url": "/profile/card_binder"},
            {"name": "Favoritos", "url": "/profile/favs"},
            {"name": "Cerrar Sesión", "url": "/auth/logout"},
        ],
    },
    {"name": "Buscador", "url": "/cards"},
    {"name": "Decks", "url": "/decks"},
    {"name": "Editor", "url": "/deck_editor"},
    {"name": "Torneos", "url": "/tournaments"},
    {"name": "Crear Torneo", "url": "/submit_tournament"},
    {"name": "Formatos", "url": "/formats"},
]
