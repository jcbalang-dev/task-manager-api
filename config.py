from dotenv import dotenv_values

env = dotenv_values()

class Config:
    """ environment variables """ 
    # MySQL connection
    DB_HOST = env.get('DB_HOST', 'localhost')
    DB_USER = env.get('DB_USER')
    DB_PASSWORD = env.get('DB_PASSWORD')
    DB_DATABASE = env.get('DB_DATABASE')

    # ssh flag
    USE_SSH = bool(env.get('USE_SSH',False))
    USE_SSH_PASSWORD = bool(env.get('USE_SSH_PASSWORD', False))

    # mysql ssh connection
    MYSQL_PORT = int(env.get('MYSQL_PORT'))
    
    SSH_HOST = env.get('SSH_HOST')
    SSH_PORT = int(env.get('SSH_PORT', 22))
    SSH_POOL_NAME = env.get('SSH_POOL_NAME','mydbpool')
    SSH_POOL_SIZE = int(env.get('SSH_POOL_SIZE', 5))
    SSH_USERNAME = env.get('SSH_USERNAME')
    SSH_PASSWORD = env.get('SSH_PASSWORD','')
    SSH_PRIVATE_KEY_PATH = env.get('SSH_PRIVATE_KEY_PATH','')

    # server port
    API_PORT = int(env.get('API_PORT', 5000))
