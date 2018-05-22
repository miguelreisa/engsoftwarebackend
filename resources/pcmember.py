

import sqlite3
from flask_restful import Resource, reqparse
from models.conference import ConferenceModel
from models.user import UserModel
from models.token import TokenModel
from models.pcmember import PCMemberModel


class PCMember(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('tokenId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('conferenceMember',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('pcmemberUsername',
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
        data = PCMember.parser.parse_args()

        chair = UserModel.find_by_username(data['conferenceMember'])
        if chair:
            chairToken = TokenModel.find_by_username(data['conferenceMember'])
            if chairToken:
                if chairToken.tokenId == data['tokenId']:
                    conference = ConferenceModel.find_by_id(data['conferenceId'])
                    if conference is None:
                        return {"message" : "Conference selected doesn't exist."}, 400

                    conferencePCMembers = conference.getPCMembers()
                    for pcmember in conferencePCMembers:
                        if pcmember.userId == data['conferenceMember']:

                            if UserModel.find_by_username(data['pcmemberUsername']) is None:
                                return {"message" : "User selected to add doesn't exist."}, 400

                            conferencesThatUserSelectIsPCMember = PCMemberModel.find_by_username(data['pcmemberUsername'])
                            for membership in conferencesThatUserSelectIsPCMember:
                                if membership.conference_id == data['conferenceId']:
                                    return {'message' : 'User {} is already a PC Member of this conference.'.format(data['pcmemberUsername'])}, 400

                            pcmember = PCMemberModel(data['pcmemberUsername'], data['conferenceId'])
                            pcmember.save_to_db()
                            return {'message' : 'User {} added as a PC Member!'.format(data['pcmemberUsername'])}, 201
                        else:
                            return {"message" : "You are not a PC Member of this conference."}, 400
        #return {"message":"An error occurred, if this continues please contact us."}, 500


        return {'message' : 'Invalid input.'}, 403
