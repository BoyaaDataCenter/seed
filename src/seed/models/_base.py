from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

__all__ = ['db', 'migrate', 'BaseModel']


db = SQLAlchemy()
migrate = Migrate()


class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)