import sqlite3
from flask_restful import Resource, reqparse
from models.conference import ConferenceModel
from models.paper import PaperModel
from models.user import UserModel
from models.token import TokenModel

class Paper(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument('tokenId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('paperName',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('author',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('content',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('conferenceId',
        type = int,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('linkCode',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )

    def post(self):
        data = Paper.parser.parse_args()

        user = UserModel.find_by_username(data['author'])
        if user:
            userToken = TokenModel.find_by_username(data['author'])
            if userToken:
                if userToken.tokenId == data['tokenId']:
                    #if PaperModel.find_by_name(data['paperName']):
                        #return {"message" : "Paper with that name already exists."}, 400
                    conference_selected = ConferenceModel.find_by_id(data['conferenceId'])
                    if conference_selected is None:
                        return {"message" : "Conference selected doesn't exist."}, 400

                    if conference_selected.linkCode != data['linkCode']:
                        return {"message" : "Conference Link Code provided incorrect, please ask the conference's chair for the code."}, 403

                    paper = PaperModel(data['paperName'], data['author'], data['content'], data['conferenceId'])
                    paper.save_to_db()
                    return {'message' : 'Paper accepted and created!'}, 201
        #return {"message":"An error occurred, if this continues please contact us."}, 500


        return {'message' : 'Invalid input.'}, 403



class PaperList(Resource):
    def get(self):
        return {'papers' : [paper.json() for paper in PaperModel.query.all()] } #devolve todos os objectos na db
