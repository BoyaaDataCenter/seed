import json
from datetime import datetime

from flask import g
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import sqltypes
from sqlalchemy.ext.declarative import declared_attr

from flask_sqlalchemy import SQLAlchemy, BaseQuery, orm

from seed.utils.time import convert_utc_to_local

__all__ = ['db', 'ma', 'migrate', 'session', 'BaseModel', 'BussinessModel']


DEFAULT_DATETIME = '1970-01-01 00:00:00'


class SeedQuery(BaseQuery):
    def __init__(self, *args, **kwargs):
        super(SeedQuery, self).__init__(*args, **kwargs)

    def as_list(self, *clolumns):
        return [{key: getattr(row, key, None) for key in row.keys()} for row in self]


class SessionMixin(object):
    column_filter = []

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def flush(self):
        db.session.flush(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name in self.column_filter:
                continue

            if isinstance(column.type, sqltypes.DateTime):
                local_time = convert_utc_to_local(getattr(self, column.name), 'Asia/Shanghai')
                d[column.name] = local_time.strftime('%Y-%m-%d %H:%M:%S') if local_time else DEFAULT_DATETIME
            else:
                d[column.name] = getattr(self, column.name)
        return d


db = SQLAlchemy(query_class=SeedQuery)
migrate = Migrate()
session = orm.scoped_session(orm.sessionmaker(autocommit=True))
ma = Marshmallow()


class BaseModel(db.Model, SessionMixin):
    __abstract__ = True
    column_filter = ['created', 'updated']

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow()
    )
    updated = db.Column(
        db.DateTime, default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    def delete(self):
        if hasattr(self, 'status'):
            self.status = -1
            self.save()
        else:
            super(BaseModel, self).delete()


class BussinessModel(BaseModel):
    """ 与业务绑定的Model
    """
    __abstract__ = True
    column_filter = ['created', 'updated', 'bussiness_id']

    @declared_attr
    def bussiness_id(cls):
        return db.Column(db.Integer, db.ForeignKey('bussiness.id'))

    def __init__(self, *args, **kwargs):
        self.bussiness_id = g.bussiness_id
        super(BussinessModel, self).__init__(*args, **kwargs)


class PageModel(BussinessModel):
    """ 与页面绑定的Model
    """
    __abstract__ = True

    column_filter = ['created', 'updated', 'bussiness_id', 'page_id']

    @declared_attr
    def page_id(cls):
        return db.Column(db.Integer, db.ForeignKey('menu.id'))