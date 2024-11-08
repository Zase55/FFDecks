from flask import Flask, render_template, request # type: ignore
from markupsafe import escape # type: ignore
from card.entity import Card

app = Flask(__name__)
cards = []

# Definir un menú con enlaces y nombres
menu_items = [
    {'name': 'Inicio', 'url': '/'},
    {
        'name': 'Perfil', 'url': '#',
        'submenu': [
            {'name': 'Decks', 'url': '/profile/my_decks'},
            {'name': 'Torneos', 'url': '/profile/my_tournaments'},
            {'name': 'Mis Cartas', 'url': '/profile/card_binder'},
            {'name': 'Favoritos', 'url': '/profile/favs'}
        ]
     },
    {'name': 'Buscador', 'url': '/card_finder'},
    {'name': 'Decks', 'url': '/decks'},
    {'name': 'Editor', 'url': '/deck_editor'},
    {'name': 'Torneos', 'url': '/tournaments'},
    {'name': 'Crear Torneo', 'url': '/submit_tournament'},
    {'name': 'Formatos', 'url': '/formats'}
]

@app.route('/')
def home():
    return render_template('menu.html', menu=menu_items, title="Inicio")

@app.route('/profile')
def profile():
    return render_template('menu.html', menu=menu_items, title="Perfil")

@app.route('/profile/my_decks')
def my_decks():
    return render_template('menu.html', menu=menu_items, title="Decks")

@app.route('/profile/my_tournaments')
def my_tournaments():
    return render_template('menu.html', menu=menu_items, title="Torneos")

@app.route('/profile/card_binder')
def card_binder():
    return render_template('menu.html', menu=menu_items, title="Mis Cartas")

@app.route('/profile/favs')
def favs():
    return render_template('menu.html', menu=menu_items, title="Favoritos")

@app.route('/card_finder')
def card_finder():
    return render_template('menu.html', menu=menu_items, title="Buscador de Cartas")

@app.route('/decks')
def decks():
    return render_template('menu.html', menu=menu_items, title="Decks")

@app.route('/deck_editor')
def deck_editor():
    return render_template('menu.html', menu=menu_items, title="Editor de Decks")

@app.route('/tournaments')
def tournaments():
    return render_template('menu.html', menu=menu_items, title="Torneos")

@app.route('/submit_tournament')
def submit_tournament():
    return render_template('menu.html', menu=menu_items, title="Crear Torneo")

@app.route('/formats')
def formats():
    return render_template('menu.html', menu=menu_items, title="Formatos")

@app.route('/cards', methods=['POST'])
def add_card():
    data = request.get_json()
    cards.append(data)
    return cards

@app.route('/cards', methods=['GET'])
def cards():
    return cards

if __name__ == '__main__':
    app.run(debug=True)
