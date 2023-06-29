import mysql.connector.pooling
from config import Config
from sshtunnel import SSHTunnelForwarder


class Database:
    connection_pool = None
    ssh_tunnel = None
    
    @classmethod
    def initialize(cls):
        # MySQL connection
        db_host = Config.DB_HOST
        db_user = Config.DB_USER
        db_password = Config.DB_PASSWORD
        db_database = Config.DB_DATABASE

        # mysql ssh connection
        mysql_port = Config.MYSQL_PORT

        # ssh flag
        use_ssh = Config.USE_SSH
        use_ssh_password = Config.USE_SSH_PASSWORD 

        ssh_host = Config.SSH_HOST
        ssh_port = Config.SSH_PORT
        ssh_pool_name = Config.SSH_POOL_NAME
        ssh_pool_size = Config.SSH_POOL_SIZE
        ssh_username = Config.SSH_USERNAME
        ssh_password = Config.SSH_PASSWORD
        ssh_private_key_path = Config.SSH_PRIVATE_KEY_PATH

        if use_ssh:
            # Create SSH Tunnel
            cls.ssh_tunnel = SSHTunnelForwarder(
                (ssh_host, ssh_port) ,
                ssh_username = ssh_username ,
                ssh_password = ssh_password ,
                ssh_pkey = ssh_private_key_path if use_ssh_password and use_ssh_password !='' else ssh_password,
                remote_bind_address = (db_host, mysql_port)
            )

            cls.ssh_tunnel.start()

            #connection using SSH
            db_config = {
                'pool_name'             : ssh_pool_name ,
                'pool_size'             : ssh_pool_size ,
                'host'                  : 'localhost' ,
                'port'                  : cls.ssh_tunnel.local_bind_port ,
                'user'                  : db_user ,
                'password'              : db_password ,
                'database'              : db_database ,
                'unix_socket'           : '' ,
                'ssl_disabled'          : True ,
                'use_pure'              : True ,
                'allow_local_infile'    : True ,
                'ssl_verify_cert'       : False
            }

            cls.connection_pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)

        else:
            # connection without SSH
            cls.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name = ssh_pool_name ,
                pool_size = ssh_pool_size ,
                host = db_host ,
                user = db_user ,
                password = db_password ,
                database = db_database
            )

    @classmethod
    def get_connection(cls):
        return cls.connection_pool.get_connection()
    
    @classmethod
    def close_pool(cls):
        cls.connection_pool.closeall()
        if cls.ssh_tunnel:
            cls.ssh_tunnel.stop()
