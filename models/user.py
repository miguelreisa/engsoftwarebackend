import sqlite3
from db import db

class UserModel(db.Model): #este extends diz ao SQLAlchemy Entity que estas classes (que tem este extends) vao ser guardadas na DB

	__tablename__ = 'users' #table name na db

	#colunas que a tabela tem
	id = db.Column(db.Integer, primary_key=True) #id é integer e é primary key. nao e problema usar apenas 'id' aqui
	username = db.Column(db.String(80)) #80 é o size limit
	password = db.Column(db.String(80))

	#nao se esta a colocar _id nos params porque é colocado automaticamente na DB com auto increment
	#quando se vai buscar (queries) vem com o id mas ignoramos??
	def __init__(self, username, password):
		#estas props tem que ser iguais as colocadas nas colunas em cima
		self.username = username
		self.password = password

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod #visto que nao usamos o self
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()

	@classmethod #visto que nao usamos o self
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()
