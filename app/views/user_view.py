from flask import jsonify

class UserView:
    @staticmethod
    def serialize_user(user):
        return {
            'id'            : user.id ,
            'role_id'       : user.role_id ,
            'last_name'     : user.last_name ,
            'first_name'    : user.first_name ,
            'username'      : user.username ,
            'email'         : user.email ,
            'password'      : user.password ,
            'created_at'    : user.created_at ,
            'updated_at'    : user.updated_at 
        }
    
    @staticmethod
    def render_user(user):
        return jsonify(UserView.serialize_user(user))
    
    def render_users(users):
        result = []
        for user in users:
            user_dict = {
                'id': user[0],
                'role_id': user[1],
                'last_name': user[2],
                'first_name': user[3],
                'middle_name': user[4],
                'username': user[5],
                'email': user[6],
                'password': user[7],
                'created_at': user[8],
                'updated_at': user[9]
            }
            result.append(user_dict)

        return {'users': result}