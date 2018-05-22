from db import db

class ItemModel(db.Model): #este extends diz ao SQLAlchemy Entity que estas classes (que tem este extends) vao ser guardadas na DB

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) #store a que pertence. com foreign key para a tabela stores. ao ter foreign key, para eliminarmos a store tinhamos que elimnar os items "ligados" primeiro

    store = db.relationship('StoreModel') #sabe logo que ha uma StoreModel que faz match ao store_id de cada item #ligado a uma store apenas #many to one

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name' : self.name, 'price' : self.price}

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
