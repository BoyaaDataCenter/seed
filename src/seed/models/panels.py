from seed.models._base import db, PageModel

__all__ = ['Panels']


class Panels(PageModel):
    """ data panels model
    """
    name = db.Column(
        db.Text, nullable=False,
        comment='Panel name'
    )

    desc = db.Column(
        db.Text, nullable=False,
        comment='Panel description'
    )

    x = db.Column(
        db.Float, nullable=False,
        comment='The panel x coordinate'
    )

    y = db.Column(
        db.Float, nullable=False,
        comment='The panel y coordinate'
    )

    w = db.Column(
        db.Float, nullable=False,
        comment='The panel width'
    )

    h = db.Column(
        db.Float, nullable=False,
        comment='The panel height'
    )

    db_source = db.Column(
        db.Integer, nullable=False,
        comment='Panel sql query database id'
    )

    charttype = db.Column(
        db.Text, nullable=False,
        comment='Panel data chart type'
    )

    sql = db.Column(
        db.Text, nullable=False,
        comment='Panel sql string'
    )

    indexs = db.Column(
        db.Text, nullable=False,
        comment='Data index json configure'
    )

    dimensions = db.Column(
        db.Text, nullable=False,
        comment='Data dimensions configure'
    )

    sort = db.Column(
        db.Integer, nullable=False,
        comment='The panel sort'
    )