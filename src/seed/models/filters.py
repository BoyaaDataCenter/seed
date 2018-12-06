from seed.models._base import db, PageModel

__all__ = ['Filters']


class Filters(PageModel):
    """ Filter model class
    """
    belong_id = db.Column(
        db.Integer,
        comment='Filter belong which model'
    )
    dtype = db.Column(
        db.Text, nullable=False,
        comment='Filter belong type, page or model'
    )
    stype = db.Column(
        db.Text, nullable=False,
        default='single', comment='Single or mulitple choice'
    )
    ename = db.Column(
        db.Text, nullable=False,
        comment='Field english name'
    )
    cname = db.Column(
        db.Text, nullable=False,
        comment='Field chinese name'
    )
    cascades = db.Column(
        db.Text, default=0,
        comment='The Filter field cascade id if it exists'
    )
    db_source = db.Column(
        db.Integer,
        comment='The filter data query database id only for sql'
    )
    condition_type = db.Column(
        db.Text, nullable=False,
        comment='The Filter condition setting type, manual or sql'
    )
    conditions = db.Column(
        db.Text, nullable=False,
        comment='The Filter conditions, it will save as json string'
    )
    sort = db.Column(
        db.Integer, default=0,
        comment='The filter sort'
    )
