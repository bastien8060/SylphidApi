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
from app.models.models import User

from app import resp_handler

from typing import List, Tuple

import secrets

import json

import re


# Define the blueprint: 'dates', set its url prefix: app.url/dates
mod_games = Blueprint('games', __name__, url_prefix='/api/v1/games')


@mod_games.route('/', methods=['GET', 'POST'])
def list():
    print(1)
    # function to list all available games (with its partner)

    try:
        #auth = request.headers.get('Authorization')
        #username,token = pry_authorization(auth)

        #status, user = verify_token(username,token)
        status = True # dummy data (mockup) for now

        if status:
            # dummy data (mockup) for now
            data = [
                {'name': "Dungeons and Dragons", 'description': "A classic role-playing game", 'id': 1},
                {'name': "Conversation Starter", 'description': "Kindles spicy and interesting conversations", 'id': 2},
                {'name': "Truth or Dare", 'description': "A classic party game for couples", 'id': 3},
                {'name': "20 Questions", 'description': "To guess the object in 20 questions or less", 'id': 4},
                {'name': "Truth Be Told", 'description': "You both have to answer the question. The best answer wins!", 'id': 5},
                {'name': "Complete the Story", 'description': "Use teamwork to complete the prompt story.", 'id': 6},
            ]

            return resp_handler.get_handler("response_ok", {"data": data})
        return resp_handler.get_handler("token_auth")
    except:
        pass

    return resp_handler.get_handler("unhandled_error", "Missing username/secret")

