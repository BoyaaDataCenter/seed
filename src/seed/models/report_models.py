from . import db, BaseModel

__all__ = ['ReportModels']


class ReportModels(BaseModel):
    """ Report form model setting
    """
    __tablename__ = 'report_model'

    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))

    coordinate_x = db.Column(db.Integer, nullable=False,
        comment='The report model coordinate x in page')
    coordinate_y = db.Column(db.Integer, nullable=False,
        comment='The report model coordinate y in page')

    name = db.Column(db.Text, nullable=False,
        comment='Report model name')
    charttype = db.Column(db.Text, nullable=False,
        comment='Report model chart type')

    description = db.Column(db.Text, comment='Report model description')

    query_sql = db.Column(db.Text, nullable=False,
        comment='Report model query sql')