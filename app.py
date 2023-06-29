from flask import Flask
from flask_restful import Api
from dotenv import dotenv_values
from db import Database
from config import Config

# Initialize database connection
Database.initialize()

from app.controllers.user_controller import UserController, UserDetailController

# Load environment variables from .env 
env = dotenv_values()

# server port
api_port = Config.API_PORT

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

# add resource routes
app.add_url_rule( '/users', view_func = UserDetailController.as_view('users') )
api.add_resource( UserController, '/user/<int:user_id>')

# application run
if __name__=='__main__':
    app.run( host='0.0.0.0', port = api_port, debug=True )

# Close database connection pool
Database.close_pool()