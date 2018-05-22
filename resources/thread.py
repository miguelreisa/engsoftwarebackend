import sqlite3
from flask_restful import Resource, reqparse
from models.conference import ConferenceModel
from models.paper import PaperModel
from models.user import UserModel
from models.token import TokenModel
from models.thread import ThreadModel
from models.threadresponse import ThreadResponseModel

class ThreadResponses(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tokenId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('messageAuthor',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('messageContent',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )

    def get(self, threadId):
        thread = ThreadModel.find_by_id(threadId)
        if thread:
            return thread.json2()
        return {'message' : 'Thread not found'}, 404

    def post(self, threadId):
        data = ThreadResponses.parser.parse_args()

        user = UserModel.find_by_username(data['messageAuthor'])
        if user:
            userToken = TokenModel.find_by_username(data['messageAuthor'])
            if userToken:
                if userToken.tokenId == data['tokenId']:
                    #if PaperModel.find_by_name(data['paperName']):
                        #return {"message" : "Paper with that name already exists."}, 400
                    thread_selected = ThreadModel.find_by_id(threadId)
                    if thread_selected is None:
                        return {"message" : "Thread selected doesn't exist."}, 400


                    thread_response = ThreadResponseModel(data['messageAuthor'], data['messageContent'], threadId)
                    thread_response.save_to_db()
                    return {'message' : 'Thread response accepted and created!'}, 201
        #return {"message":"An error occurred, if this continues please contact us."}, 500


        return {'message' : 'Invalid input.'}, 403

class Thread(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tokenId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('threadAuthor',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('topic',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('conferenceId',
        type = int,
        required = True,
        help = "This field cannot be left blank!"
    )

    def post(self):
        data = Thread.parser.parse_args()

        user = UserModel.find_by_username(data['threadAuthor'])
        if user:
            userToken = TokenModel.find_by_username(data['threadAuthor'])
            if userToken:
                if userToken.tokenId == data['tokenId']:
                    #if PaperModel.find_by_name(data['paperName']):
                        #return {"message" : "Paper with that name already exists."}, 400
                    conference_selected = ConferenceModel.find_by_id(data['conferenceId'])
                    if conference_selected is None:
                        return {"message" : "Conference selected doesn't exist."}, 400


                    thread = ThreadModel(data['threadAuthor'], data['topic'], data['conferenceId'])
                    thread.save_to_db()
                    return {'message' : 'Thread accepted and created!'}, 201
        #return {"message":"An error occurred, if this continues please contact us."}, 500


        return {'message' : 'Invalid input.'}, 403
