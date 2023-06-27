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


if __name__=='__main__':
    app.run( host='0.0.0.0', port = api_port )

# close MySQL cursor and connection
db_cursor.close()
db_connection.close()

# close SSH connection
if use_ssh:
    tunnel.stop()