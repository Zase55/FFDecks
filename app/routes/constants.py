menu_items = [
    {'name': 'Inicio', 'url': '/auth'},
    {'name': 'Buscador', 'url': '/api/card_finder'},
    {'name': 'Decks', 'url': '/api/decks'},
    {'name': 'Editor', 'url': '/api/deck_editor'},
    {'name': 'Torneos', 'url': '/api/tournaments'},
    {'name': 'Crear Torneo', 'url': '/api/submit_tournament'},
    {'name': 'Formatos', 'url': '/api/formats'},
    {'name': 'Login', 'url': '/auth/login'},
    {'name': 'Registrarse', 'url': '/auth/register'}
]

menu_items_login = [
    {'name': 'Inicio', 'url': '/auth'},
    {
        'name': 'Perfil', 'url': '#',
        'submenu': [
            {'name': 'Decks', 'url': '/api/profile/my_decks'},
            {'name': 'Torneos', 'url': '/api/profile/my_tournaments'},
            {'name': 'Mis Cartas', 'url': '/api/profile/card_binder'},
            {'name': 'Favoritos', 'url': '/api/profile/favs'},
            {'name': 'Cerrar Sesión', 'url': '/auth/logout'}
        ]
     },
    {'name': 'Buscador', 'url': '/api/card_finder'},
    {'name': 'Decks', 'url': '/api/decks'},
    {'name': 'Editor', 'url': '/api/deck_editor'},
    {'name': 'Torneos', 'url': '/api/tournaments'},
    {'name': 'Crear Torneo', 'url': '/api/submit_tournament'},
    {'name': 'Formatos', 'url': '/api/formats'}
]