from flask import Flask
from dotenv import dotenv_values
import mysql.connector
import paramiko
from sshtunnel import SSHTunnelForwarder

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

#mysql ssh connection
mysql_port = int(env['MYSQL_PORT'])

use_ssh = bool(env.get('USE_SSH','False'))
use_ssh_password = bool(env.get('USE_SSH_PASSWORD','False'))

ssh_host = env['SSH_HOST']
ssh_username = env['SSH_USERNAME']
ssh_password = env.get('SSH_PASSWORD', '')
ssh_private_key_path = env.get('SSH_PRIVATE_KEY_PATH','')


app = Flask(__name__)

# MySQL connection
if use_ssh:
    # create SSH tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        ssh_pkey= ssh_private_key_path if use_ssh_password and use_ssh_password !='' else ssh_password,
        remote_bind_address=(db_host, mysql_port)
    )

    tunnel.start()

    #connection using SSH
    db_config = {
        'user'                  : db_user,
        'password'              : db_password,
        'host'                  : 'localhost',
        'port'                  : tunnel.local_bind_port,
        'database'              : db_database,
        'unix_socket'           : '',
        'ssl_disabled'          : True,
        'use_pure'              : True,
        'allow_local_infile'    : True,
        'ssl_verify_cert'       : False
    }
    
    db_connection = mysql.connector.connect(**db_config)
else:
    # connection without SSH
    db_connection = mysql.connector.connect(
        host = db_host ,
        user = db_user ,
        password = db_password ,
        database = db_database
    )

# create a cursor
db_cursor = db_connection.cursor()

# NOTE!!!
# Please remove this code once MVC is established

@app.get("/roles")
def get_roles():
    query = 'select * from role'
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

@app.get("/users")
def get_users():
    query = 'select * from user'
    db_cursor.execute(query)
    users = db_cursor.fetchall()

    result = []
    for user in users:
        user_dict = {
            'id' : user[0] ,
            'role_id' : user[1] ,
            'last_name' : user[2] ,
            'first_name' : user[3] ,
            'middle_name' : user[4] ,
            'username' : user[5] ,
            'email' : user[6] ,
            'password' : user[7] ,
            'created_at' : user[8] ,
            'updated_at' : user[9]
        }
        result.append(user_dict)

    return {
        'users' : result
    }

if __name__=='__main__':
    app.run( host='0.0.0.0', port = api_port )

# close MySQL cursor and connection
db_cursor.close()
db_connection.close()

# close SSH connection
if use_ssh:
    tunnel.stop()