#Contem funcoes importantes para a segurança
from werkzeug.security import safe_str_cmp #compara strings em vez do == (mais seguro?) é mesmo necessario se estivermos a usar python 2.7 por ex
from models.user import UserModel

# VERSAO HARDCODED ESTA NA SECCAO 4


def authenticate(username,password):
	user = UserModel.find_by_username(username) #se nao encontrar devolve None
	if user and safe_str_cmp(user.password,password): #equivalente a if user not None and user.password = password
		return user

def identity(payload):
	user_id = payload['identity']
	return UserModel.find_by_id(user_id)
