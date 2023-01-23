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

from app import resp_handler

from typing import List, Tuple

import secrets

import json

import re

import requests


# Define the blueprint: 'dates', set its url prefix: app.url/dates
mod_game_truthordare = Blueprint('game_truthordare', __name__, url_prefix='/api/v1/games/truthordare')

@mod_game_truthordare.route('/', methods=['GET', 'POST'])
def list():
    # function to list all truth or dare questions

    try:
        #auth = request.headers.get('Authorization')
        #username,token = pry_authorization(auth)

        #status, user = verify_token(username,token)
        status = True # dummy data (mockup) for now

        if status:
            resp = requests.get('https://raw.githubusercontent.com/sylhare/Truth-or-Dare/master/src/output.json')
            data = resp.json()

            return resp_handler.get_handler("response_ok", {"data": data})
        return resp_handler.get_handler("token_auth")
    except:
        pass

    return resp_handler.get_handler("unhandled_error", "Missing username/secret")

@mod_game_truthordare.route('/drawcard/<username>/<id>/<type>', methods=['GET', 'POST'])
def drawcard(username, id, type):
    # function to draw a card from the deck

    try:
        #auth = request.headers.get('Authorization')
        #username,token = pry_authorization(auth)

        #status, user = verify_token(username,token)
        status = True # dummy data (mockup) for now

        if status:
            #add new entry to history
            new_history = TruthDareHistory(
                cardID = int(id),
                type = type,
                username = username
            )
            db.session.add(new_history)
            db.session.commit()

            return resp_handler.get_handler("response_ok", {"data": {
                'cardID': new_history.cardID,
                'type': new_history.type,
                'username': new_history.username
            }})
        return resp_handler.get_handler("token_auth")
    except:
        pass

    return resp_handler.get_handler("unhandled_error", "Errrorrr")

#get last card
@mod_game_truthordare.route('/history/last', methods=['GET', 'POST'])
def lastcard():
    # function to get last card

    try:
        #auth = request.headers.get('Authorization')
        #username,token = pry_authorization(auth)

        #status, user = verify_token(username,token)
        status = True # dummy data (mockup) for now

        if status:
            #get last entry from history
            last_history = TruthDareHistory.query.order_by(TruthDareHistory.id.desc()).first()

            return resp_handler.get_handler("response_ok", {"data": {
                'cardID': last_history.cardID,
                'type': last_history.type,
                'username': last_history.username

            }})
        return resp_handler.get_handler("token_auth")
    except:
        pass
    
    return resp_handler.get_handler("unhandled_error", "Errrorrr")

@mod_game_truthordare.route('/history', methods=['GET', 'POST'])
def history():
    # function to get all history

    try:
        #auth = request.headers.get('Authorization')
        #username,token = pry_authorization(auth)

        #status, user = verify_token(username,token)
        status = True # dummy data (mockup) for now

        if status:
            #get all history
            history = TruthDareHistory.query.all()

            history_dict = []

            for h in history:
                history_dict.append({
                    'cardID': h.cardID,
                    'type': h.type,
                    'username': h.username
                })

            return resp_handler.get_handler("response_ok", {"data": {
                'history': history_dict
            }})
        return resp_handler.get_handler("token_auth")
    except:
        pass



        