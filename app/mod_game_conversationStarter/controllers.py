# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from sqlalchemy import or_
from unidecode import unidecode

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_updates.forms import LoginForm, RegisterForm, VerifyForm

# Import module models (i.e. User)
from app.models.models import User, TruthDareHistory

from app.stores import api_store

from app import resp_handler

from typing import List, Tuple

import secrets

import json

import re

import requests


# Define the blueprint: 'dates', set its url prefix: app.url/dates
mod_game_conversationStarter = Blueprint('game_conversationStarter', __name__, url_prefix='/api/v1/games/conversation_starter')

@mod_game_conversationStarter.route('/get', methods=['GET', 'POST'])
def list():
    # function to list all conversations questions

    try:
        #auth = request.headers.get('Authorization')
        #username,token = pry_authorization(auth)

        #status, user = verify_token(username,token)

        return resp_handler.get_handler("response_ok", {"data": api_store.topics})
    except:
        pass

    return resp_handler.get_handler("unhandled_error", "Missing username/secret")

@mod_game_conversationStarter.route('/topics', methods=['GET', 'POST'])
def get_topics():
    try:

        return resp_handler.get_handler("response_ok", {"data": api_store.topics_map})
    except:
        pass
        