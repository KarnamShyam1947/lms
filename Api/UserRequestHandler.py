from flask_restful import Resource, abort
from flask import request
from app import db
from models import *

class UserRequestHandler(Resource):
    def get(self, id):
        user = User.query.filter_by(id = id).first()
        type = request.args.get('type')
        print(type)

        if type:
            if user:
                user.isAdmin = type
                if type == 1:
                    user.isVerified = 1

                db.session.commit()

                return {
                    'status' : 'success',
                    'code' : 200,
                }

            else:
                abort(404)

        else:
            abort(404)


    def delete(self, id):
        user = User.query.filter_by(id = id).first()

        if user:
            db.session.delete(user)
            db.session.commit()

            return {
                'status' : 'success',
                'code' : 200,
            }
        
        else:
            abort(404)

    