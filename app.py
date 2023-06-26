from flask import Flask
from dotenv import dotenv_values
import mysql.connector

# Load environment variables from .env 
env = dotenv_values()

# environment variables
# server port
api_port = int(env['PORT_NUMBER'])

# MySQL connection
db_host = env['DB_HOST']
db_user = env['DB_USER']
db_password = env['DB_PASSWORD']
db_database = env['DB_DATABASE']

app = Flask(__name__)

# MySQL connection
db_connection = mysql.connector.connect(
    host = db_host ,
    user = db_user ,
    password = db_password ,
    database = db_database
)

def get_roles():
    query = "select * from roles"
    db_cursor.execute(query)
    roles = db_cursor.fetchall()

    result = []
    for role in roles:
        role_dict = {
            'id' : role[0] ,
            'title' : role[1] ,
            'slug' : role[2] ,
            'description' : role[3]
        }
        result.append(role_dict)

    return {
        'roles': result
    }

# create a cursor
db_cursor = db_connection.cursor()


if __name__=='__main__':
    app.run( host='0.0.0.0', port = api_port )

# close MySQL cursor and connection
db_cursor.close()
db_connection.close()