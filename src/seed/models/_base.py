from datetime import datetime

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_migrate import Migrate

__all__ = ['db', 'migrate', 'BaseModel']



class SeedQuery(BaseQuery):
    def __init__(self, *args, **kwargs):
        super(SeedQuery, self).__init__(*args, **kwargs)


db = SQLAlchemy(query_class=SeedQuery)
migrate = Migrate()


class BaseModel(db.Model):
    __abstract__ = True

    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow()
    )
    updated = db.Column(
        db.DateTime, onupdate=datetime.utcnow()
    )

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)