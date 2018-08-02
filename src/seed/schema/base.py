from marshmallow_sqlalchemy import ModelSchema

from seed.models._base import session, ma

class BaseSchema(ma.ModelSchema):

    class Meta:
        sqla_session = session