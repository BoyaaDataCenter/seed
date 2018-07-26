from flask.ext.sqlalchemy import SQLAlchemy

__all__ = ['db', 'BaseModel']


db = SQLAlchemy()


class BaseModel(db.Model):

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
