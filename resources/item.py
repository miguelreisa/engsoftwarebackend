from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

	#Isto pode tar num metodo mas assim escusamos de copiar codigo
	parser = reqparse.RequestParser() #passar pelo request e ver que argumentos fazem match dos que queremos. Pega nas variaveis do body do request para fazer parse
	#Por exemplo: ao colocar aqui o price com required=True, se nao for dado no body do request, devolve a msg em help
	parser.add_argument('price',
		type=float, #qd davamos 12.00 ficava 12, assim resolve o problema
		required = True, #termina se nao tiver o field (nao continua metodo)
		help="This field cannot be left blank!"
		#pode haver mts mais para ajudar no parse
	)
	parser.add_argument('store_id',
		type=int,
		required=True,
		help="Every item needs a store id"
	)

	@jwt_required() #user precisa de estar autenticado antes de chamar o get, devolve chamada de erro se nao for dado um token. pode ser usado em qualquer lado
	def get(self,name):

		item = ItemModel.find_by_name(name)
		if item:
			return item.json() #visto que o find_by_name devolve object, temos que transformar em json

		return {'message' : 'Item not found'}, 404

	def post(self,name): #post method tem que ter o mesmo set de parametros que o get mesmo que tenha json payload

		if ItemModel.find_by_name(name):
			return {'message' : 'An item with name {} already exists'.format(name)}, 400 #Bad request

		#request_data = request.get_json()  #SEM PARSER
		request_data = Item.parser.parse_args() #faz parse dos args que vem no payload. Como se colocou o parser mesmo nesta classe Item, temos que colcoar Item.parser.etc

		item = ItemModel(name,request_data['price'], request_data['store_id']) ##ou **request_data

		try: #colocar isto em varios sitios onde pode dar erro, principalmente em metodos que envolvam a DB
			item.save_to_db() #adiciona-se a si proprio
		except:
			return {"message" : "An error occurred inserting the item."}, 500

		return item.json() , 201 # ja nao e preciso jsonify, flask restful faz isso por nos. 202 é usado qd ha delay na criaçao (se aceitou o pedido mas so vai criar dps)

	def delete(serlf, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message' : 'Item deleted'}

	def put(self,name):

		request_data = Item.parser.parse_args() #faz parse dos args que vem no payload. Como se colocou o parser mesmo nesta classe Item, temos que colcoar Item.parser.etc

		#Fizemos parse do request

		item = ItemModel.find_by_name(name)

		try:
			if item is None:
				item = ItemModel(name, request_data['price'], request_data['store_id']) #ou **request_data
			else:
				item.price = request_data['price']

			item.save_to_db()
		except:
			return {"message":"An error occurred inserting the item."}, 500

		return item.json()

class ItemList(Resource):
	def get(self):
		return {'items' : [item.json() for item in ItemModel.query.all()] } #devolve todos os objectos na db
