# Import flask and template operators
from flask import Flask, render_template, request, Blueprint

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

import firebase_admin

from firebase_admin import messaging

from firebase_admin import credentials

from app.flask_resp_handler import RespHandler

import logging

from flask_sock import Sock

# Define the WSGI application object
app = Flask(__name__)

sock = Sock(app)

# Configurations
app.config.from_object('config')

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

resp_handler = RespHandler(app.config['DEBUG'])

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app, session_options={'autocommit': app.config['SQLALCHEMY_DB_AUTOCOMMIT']})

#cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS'])
#firebase_admin.initialize_app(cred)

def db_session_commit(db_session):
  if not app.config['SQLALCHEMY_DB_AUTOCOMMIT']:
    db_session.commit()

# Sample HTTP 404 error handling
@app.errorhandler(404)
def not_found(_error):
    # print request.url
    print(request.url)
    return resp_handler.get_handler("not_found")

# Handle 429/API rate limit errors
@app.errorhandler(429)
def ratelimit_handler(_error):
  return resp_handler.get_handler("rate_limit_exceeded")

@app.after_request 
def after_request(response):
  # this was added to allow the app to be accessed from the frontend
  # Access-Control-Allow-Origin: * -> allows all origins
  # Access-Control-Allow-Headers: Content-Type, Authorization -> allows the authentication header/token in preflight requests
  # without allowing tokens to be sent in preflight requests, the API would return an error, and chrome would not allow the actual request
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response


# Import a module / component using its blueprint handler variable (mod_auth/mod_user_profile/mod_workexperience/mod_employer)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_dates.controllers import mod_dates as dates_module
from app.mod_updates.controllers import mod_updates as updates_module
from app.mod_partner.controllers import mod_partner as partner_module
from app.mod_games.controllers import mod_games as games_module
from app.mod_game_truthordare.controllers import mod_game_truthordare as game_truthordare_module
from app.mod_game_dnd.controllers import mod_game_dnd as game_dnd_module
from app.mod_game_story.controllers import mod_game_story as game_story_module
from app.mod_config.controllers import mod_config as config_module
from app.mod_game_conversationStarter.controllers import mod_game_conversationStarter as game_conversationStarter_module


# Register blueprint(s) imported from earlier.
app.register_blueprint(auth_module)
app.register_blueprint(config_module)
app.register_blueprint(dates_module)
app.register_blueprint(updates_module)
app.register_blueprint(partner_module)
app.register_blueprint(games_module)
app.register_blueprint(game_truthordare_module)
app.register_blueprint(game_dnd_module)
app.register_blueprint(game_story_module)
app.register_blueprint(game_conversationStarter_module)


# Build the database:
# This will create the database file using SQLAlchemy
# This is built using the models.py file, used by each blueprint



with app.app_context() as ctx:
  # Create the database
  db.create_all()
