from flask import Flask
from dotenv import dotenv_values
import mysql.connector

# Load environment variables from .env 
env = dotenv_values()

# environment variables
api_port = int(env['PORT_NUMBER'])

app = Flask(__name__)

if __name__=='__main__':
    app.run( host='0.0.0.0', port = api_port )