from app.models.db_instance import DBSingleton

db = DBSingleton.get_instance()


class Db_card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)


class Card:
    def __init__(
        self,
        number,
        rarity,
        set,
        name,
        cost,
        type,
        element,
        exburst,
        multiplayable,
        category,
        job,
        abilities,
        power,
    ):
        self.number = number
        self.rarity = rarity
        self.set = set
        self.name = name
        self.cost = cost
        self.type = type
        self.element = element
        self.exburst = exburst
        self.multiplayable = multiplayable
        self.category = category
        self.job = job
        self.abilities = abilities
        self.power = power
