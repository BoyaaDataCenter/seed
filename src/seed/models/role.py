from . import db, BussinessModel

__all__ = ['Role', ]


class Role(BussinessModel):
    role = db.Column(db.Text, default='new')

    @classmethod
    def get_roles(cls, bussiness_id=None):
        query_session = cls.query
        if bussiness_id:
            query_session = query_session.filter_by(bussiness_id=bussiness_id)

        return query_session.all()
