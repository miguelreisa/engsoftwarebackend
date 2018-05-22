
from db import db
import time
import uuid


class ThreadResponseModel(db.Model): #este extends diz ao SQLAlchemy Entity que estas classes (que tem este extends) vao ser guardadas na DB

    __tablename__ = 'thread_responses'


    id = db.Column(db.Integer, primary_key = True)
    messageAuthor = db.Column(db.String(255))
    messageContent = db.Column(db.String(500))
    creationDate = db.Column(db.Integer)
    threadId = db.Column(db.Integer, db.ForeignKey('threads.id')) #store a que pertence. com foreign key para a tabela stores. ao ter foreign key, para eliminarmos a store tinhamos que elimnar os items "ligados" primeiro

    current_milli_time = lambda: int(round(time.time() * 1000))

    def __init__(self, messageAuthor, messageContent, threadId):
        self.messageAuthor = messageAuthor
        self.messageContent = messageContent
        self.creationDate = ThreadResponseModel.current_milli_time()
        self.threadId = threadId

    def json(self):
        return {'threadResponseId' : self.id, 'messageAuthor' : self.messageAuthor, 'messageContent' : self.messageContent, 'creationDate' : self.creationDate , 'threadId' : self.threadId}


    @classmethod
    def find_by_id(cls, _id):
        #este .query vem do db.Model. Esta a fazer SELECT * From items WHERE name=name
        #ao ter first() faz Esta a fazer SELECT * From items WHERE name=name LIMIT 1 (devolve a primeira row)
        #deixa nos fazer varios filters por ex: query.filter_by(name=name).filter_by(id=1).filter_by(price=5.00) para filtrar varias coisas
        #mas e melhor fazer com parametros filter_by(name=name,id=1,price=5.00)
        #devolve ItemModel object
        return cls.query.filter_by(id=_id).first() #podia ser ItemModel.query...





    #insere-se a si proprio
    def save_to_db(self):
        #SQLAlchemy faz translate de object para row, apenas precisamos de dar o objectos
        #Isto pode ser usado para insert e update, visto que o SQLAlchemy quando faz add de um objecto(row) que ja existe na db faz update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
