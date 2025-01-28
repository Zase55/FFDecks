from app.models.db_instance import DBSingleton

db = DBSingleton.get_instance()


class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String(80), nullable=False)
    collection = db.Column(db.String(5), nullable=False)
    serial = db.Column(db.String(5), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    rarity = db.Column(db.String(80), nullable=False)
    card_set = db.Column(db.String(80), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    card_type = db.Column(db.String(80), nullable=False)
    exburst = db.Column(db.String(5), nullable=False)
    limitbreak = db.Column(db.String(5), nullable=False, default="no")
    multiplayable = db.Column(db.String(5), nullable=False)
    power = db.Column(db.Integer, nullable=True)

    elements_list = db.relationship("Element", backref="cards", lazy=True)
    job_list = db.relationship("Job", backref="cards", lazy=True)
    categories_list = db.relationship("Category", backref="cards", lazy=True)
    abilities_list = db.relationship("Ability", backref="cards", lazy=True)


class Element(db.Model):
    __tablename__ = "elements"

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey(Card.id), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(80), nullable=False)

    card = db.relationship("Card", cascade="all,delete", backref="elements")


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey(Card.id), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(80), nullable=False)

    card = db.relationship("Card", cascade="all,delete", backref="jobs")


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey(Card.id), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(80), nullable=False)

    card = db.relationship("Card", cascade="all,delete", backref="categories")


class Ability(db.Model):
    __tablename__ = "abilities"

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey(Card.id), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)
    value_type = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Text, nullable=False)

    card = db.relationship("Card", cascade="all,delete", backref="abilities")
