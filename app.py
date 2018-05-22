#Qd faz import corre o codigo todo, ou seja se houver um print nos ficheiros importados corre esse print
import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity #nosso
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') #dizer ao sqlalchemy onde encontrar o ficheiro .db (aqui dizemos que esta na root folder do projecto). Nao precisa de ser sqlite, pode ser mysql, etc
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #coiso
app.secret_key = 'miguel' #teria que ser secreto & seguro
api = Api(app)

#cria um novo endpoint /auth em que se envia username e password e sao levados ao metodo authenticate feito por nos, se der match(ver funcao authenticate), devolve o user (na func authenticate)
#este auth endpoint devolve um jwt token que pode ser enviado no proximo request feito. quando enviamos um token jwt, o jwt chama a funcao identity(colocada como param aqui) e ve o user correcto para esse token
#se conseguir fizer isso é porque o user esta autenticado e pode fazer o request
jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

#quando se corre app.run da o nome a __name__ '__main__'
#este if serve para se este ficheiro app2.py for importado noutro, nao queremos que seja corrido outra vez, ou seja, que faça start do web server
#apenas queremos que faça run quando corremos mesmo python app2.py
if __name__ == '__main__':
	from db import db #import aqui é mais correcto (devido a circular import)
	db.init_app(app)
	app.run(port=5000, debug=True) #debug: qd ha um erro obtemos uma html page pa ver o que esta mal
