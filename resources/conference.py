import sqlite3
from flask_restful import Resource, reqparse
from models.conference import ConferenceModel
from models.user import UserModel
from models.token import TokenModel
from models.pcmember import PCMemberModel

class Conference(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tokenId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('conferenceName',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('primaryArea',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('founder',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('description',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('startingDate',
        type = int,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('endDate',
        type = int,
        required = True,
        help = "This field cannot be left blank!"
    )

    def post(self):
        data = Conference.parser.parse_args()

        user = UserModel.find_by_username(data['founder'])
        if user:
            userToken = TokenModel.find_by_username(data['founder'])
            if userToken:
                if userToken.tokenId == data['tokenId']:
                    if ConferenceModel.find_by_name(data['conferenceName']):
                        return {"message" : "Conference with that name already exists."}, 400

                    conference = ConferenceModel(data['conferenceName'], data['primaryArea'], data['founder'], data['description'], data['startingDate'], data['endDate'])
                    conference.save_to_db()
                    pcmember = PCMemberModel(conference.founder, conference.id)
                    pcmember.save_to_db()
                    return {'message' : 'Conference accepted and created!', 'conference' : conference.json()}, 201
        #return {"message":"An error occurred, if this continues please contact us."}, 500


        return {'message' : 'Invalid input.'}, 403



class ConferenceList(Resource):
    def get(self):
        return {'conferences' : [conference.json() for conference in ConferenceModel.query.all()] } #devolve todos os objectos na db
