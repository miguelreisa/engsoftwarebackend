from db import db
import time
import uuid

class PaperModel(db.Model): #este extends diz ao SQLAlchemy Entity que estas classes (que tem este extends) vao ser guardadas na DB

    __tablename__ = 'papers'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(80))
    content = db.Column(db.String(1000))
    submissionDate = db.Column(db.Integer)
    conference_id = db.Column(db.Integer, db.ForeignKey('conferences.id')) #store a que pertence. com foreign key para a tabela stores. ao ter foreign key, para eliminarmos a store tinhamos que elimnar os items "ligados" primeiro

    conference = db.relationship('ConferenceModel') #sabe logo que ha uma StoreModel que faz match ao store_id de cada item #ligado a uma store apenas #many to one

    current_milli_time = lambda: int(round(time.time() * 1000))

    def __init__(self, name, author, content, conference_id):
        self.name = name
        self.author = author
        self.content = content
        self.submissionDate = PaperModel.current_milli_time()
        self.conference_id = conference_id

    def json(self):
        return {'paperId' : self.id, 'name' : self.name, 'author' : self.author, 'content' : self.content, 'submissionDate' : self.submissionDate, 'conferenceId' : self.conference_id}

    @classmethod
    def find_by_name(cls, name):
        #este .query vem do db.Model. Esta a fazer SELECT * From items WHERE name=name
        #ao ter first() faz Esta a fazer SELECT * From items WHERE name=name LIMIT 1 (devolve a primeira row)
        #deixa nos fazer varios filters por ex: query.filter_by(name=name).filter_by(id=1).filter_by(price=5.00) para filtrar varias coisas
        #mas e melhor fazer com parametros filter_by(name=name,id=1,price=5.00)
        #devolve ItemModel object
        return cls.query.filter_by(name=name).first() #podia ser ItemModel.query....

    #insere-se a si proprio
    def save_to_db(self):
        #SQLAlchemy faz translate de object para row, apenas precisamos de dar o objectos
        #Isto pode ser usado para insert e update, visto que o SQLAlchemy quando faz add de um objecto(row) que ja existe na db faz update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
