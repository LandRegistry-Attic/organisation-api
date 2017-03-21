from sqlalchemy import Column, Integer
from organisation_api.extensions import db


class Organisation(db.Model):

    __tablename__ = 'organisation'

    id = Column(Integer, primary_key=True)
    organisation_id = db.Column(db.String, nullable=False, unique=True)
    organisation_name = db.Column(db.String(50), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def get_organisation(organisation_id):
    return Organisation.query.filter(Organisation.organisation_id == organisation_id)
