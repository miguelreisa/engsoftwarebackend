from db import db
from models.paper import PaperModel
from models.pcmember import PCMemberModel
from models.thread import ThreadModel

import time
import uuid

class ConferenceModel(db.Model):

    __tablename__ = 'conferences'

    id = db.Column(db.Integer, primary_key = True)
    conferenceName = db.Column(db.String(255))
    primaryArea = db.Column(db.String(255))
    founder = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    startingDate = db.Column(db.Integer)
    endDate = db.Column(db.Integer)
    linkCode = db.Column(db.String(1000))

    papers = db.relationship('PaperModel', lazy='dynamic')
    pcmembers = db.relationship('PCMemberModel', lazy='dynamic')
    threads = db.relationship('ThreadModel', lazy='dynamic')

    def __init__(self, conferenceName, primaryArea, founder, description, startingDate, endDate):
        self.conferenceName = conferenceName
        self.primaryArea = primaryArea
        self.founder = founder
        self.description = description
        self.startingDate = startingDate
        self.endDate = endDate
        self.linkCode = uuid.uuid4().hex

    def json(self):
        return {
            'conferenceId' : self.id,
            'conferenceName' : self.conferenceName,
            'primaryArea' : self.primaryArea,
            'founder' : self.founder,
            'description' : self.description,
            'startingDate' : self.startingDate,
            'endDate' : self.endDate,
            'linkCode' : self.linkCode,
            'papers' : [paper.json() for paper in self.papers.all()],
            'pcmembers' : [pcmember.json() for pcmember in self.pcmembers.all()],
            'threads' : [thread.json() for thread in self.threads.all()]
        } #qd usamos lazy='dynamic', o self.papersOuPCmembers ja nao e lista de items mas sim um query builder

    def getPCMembers(self):
        return self.pcmembers.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod #visto que nao usamos o self
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(conferenceName=name).first()
