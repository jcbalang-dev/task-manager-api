from flask_restful import Resource, reqparse
from app.models.user_model import UserModel
from app.views.user_view import UserView

user_model = UserModel()

class UserDetailController(Resource):
    def get(self):
        users = user_model.get_all_users()
        if users:
            return UserView.render_users(users)
        else:
            return {'error', 'Data not exists'}, 404

class UserController(Resource):
    def get(self, user_id):
        user = user_model.get_user(user_id)
        if user:
            return UserView.render_user(user)
        else:
            return {'error', 'User not found'}, 404
    