from seed.models._base import session, ma


class BaseSchema(ma.ModelSchema):

    class Meta:
        sqla_session = session
        include_fk = True
