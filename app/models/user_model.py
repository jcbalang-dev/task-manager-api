from db import Database

class User:
    def __init__(self, id, role_id, last_name, first_name, middle_name, username, email, password, created_at, updated_at ):
        self.id = id
        self.role_id = role_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

class UserModel:
    def __init__(self):
        self.db_connection = Database.get_connection()

    def get_all_users(self):

        db_cursor = self.db_connection.cursor()

        query = "SELECT * FROM user"

        db_cursor.execute(query)
        users = db_cursor.fetchall()
        db_cursor.close()

        if users:
            return users
        else:
            return None
        
    def get_user(self, user_id):
        db_cursor = self.db_connection.cursor()
        
        query = "SELECT * FROM user WHERE id = %s"
        
        db_cursor.execute(query, (user_id,))
        result = db_cursor.fetchone()
        db_cursor.close()

        if result:
        
            id, role_id, last_name, first_name, middle_name, username, email, password, created_at, updated_at = result
            
            return User(
                id = id ,
                role_id = role_id ,
                last_name = last_name ,
                first_name = first_name ,
                middle_name = middle_name ,
                username = username ,
                email = email ,
                password = password ,
                created_at = created_at ,
                updated_at = updated_at 
            )
        
        else:
            return None

