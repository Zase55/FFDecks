from flask_sqlalchemy import SQLAlchemy


class DBSingleton:
    db = None

    @staticmethod
    def get_instance():
        if DBSingleton.db is None:
            DBSingleton.db = SQLAlchemy()
        return DBSingleton.db
