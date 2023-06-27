from flask import Flask
from dotenv import dotenv_values
import mysql.connector
import paramiko

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

ssh_host = env['SSH_HOST']
ssh_username = env['SSH_USERNAME']
ssh_private_key_path = env['SSH_PRIVATE_KEY_PATH']


app = Flask(__name__)

# MySQL connection
if use_ssh:
    # create ssh client
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # establish ssh connection
    ssh_client.connect(
        ssh_host ,
        username = ssh_username ,
        key_filename = ssh_private_key_path
    )

    # create an ssh tunnel and forward the MySQL port
    ssh_tunnel = ssh_client.get_transport().open_channel('direct-tcpip', (db_host, mysql_port), ('localhost', mysql_port))

    #connection using SSH
    db_connection = mysql.connector.connect(
        host = '127.0.0.1' ,
        port = mysql_port ,
        user = db_user ,
        password = db_password ,
        database = db_database ,
        unix_socket = '',
        ssl_disabled = True ,
        use_pure = True ,
        connection_time_out = 30 ,
        allow_local_infile = True ,
        ssl_verify_cert = False ,
        ssh = ssh_tunnel
    )
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
    ssh_client.close()