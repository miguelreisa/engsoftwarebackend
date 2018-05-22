from db import db

class StoreModel(db.Model): #este extends diz ao SQLAlchemy Entity que estas classes (que tem este extends) vao ser guardadas na DB

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    #ve que items tem foreign key como o seu id #ligado a varios items #one to many #lazy dynamic para na ocriar logo objectos para todos os items (fica caro se houver mts)
    #com lazy dynamic é mais lento porque sempre que se chama o metodo json feito ele tem que ir à tabela, se nao tivessemos seria mais lento a criar este objecto store e mais rapido a chamar o method jsonify
    #sem lazy dynamic é mais rpd a criar o objecto store mas metodos json sao mais lentos tradeoff
    #ver sempre qual e o melhor
    #Isto porque o SQLITE deixa que hajam items com foreign keys com ids que nao existem (nao existem stores com esses ids). MySQL por ex força a existencia. É uma das limitaçoes do sqlite. Tem que se verificar a mao caso queiramos
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name' : self.name, 'items' : [item.json() for item in self.items.all()]} #qd usamos lazy='dynamic', o self.items ja nao e lista de items mas sim um query builder

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
