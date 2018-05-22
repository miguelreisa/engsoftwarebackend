#Para devolver user objects da db

import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

	parser = reqparse.RequestParser() #passar pelo request e ver que argumentos fazem match dos que queremos. Pega nas variaveis do body do request para fazer parse
	#Por exemplo: ao colocar aqui o price com required=True, se nao for dado no body do request, devolve a msg em help
	parser.add_argument('username',
		type=str, #qd davamos 12.00 ficava 12, assim resolve o problema
		required = True, #termina se nao tiver o field (nao continua metodo)
		help="This field cannot be left blank!"
		#pode haver mts mais para ajudar no parse
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help="This field cannot be left blank!"
	)


	def post(self):

		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {"message" : "User with that username already exists."}, 400

		user = UserModel(**data) #isto equivale a ter UserModel(data['username'],data['password']). Basicamente coloca os campos todos em data nos parametros
		user.save_to_db()

		return {"message" : "User created successfully."}, 201
