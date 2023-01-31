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
from app.mod_auth.forms import LoginForm, RegisterForm, VerifyForm

# Import module models (i.e. User)
from app.models.models import User

from app import resp_handler

from typing import List, Tuple

import secrets

import base64

import re


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


def strip_username(username:str) -> str:
    # Function to strip username of illegal characters, whitespace, capitalization...
    return re.sub(r'[^a-zA-Z0-9\-\_\.]', '', username).lower()

def pry_authorization(auth:str) -> List[str]:
    # Function to split an authorization token into an username 
    # and its token/secret key
    return auth.split(":")


@mod_auth.route('/login/', methods=['GET'])
def login():
    
    username = request.args.get('username')
    password = request.args.get('password')

    if User.query.filter_by(username=username).first():
        user = User.query.filter_by(username=username).first()

        if user.password == password:
            return resp_handler.get_handler("response_ok", {"data": {
                'status': True
            }})
        else:
            return resp_handler.get_handler("response_ok", {"data": {
                'status': False
            }})
    else:
        return resp_handler.get_handler("response_ok", {"data": {
            'status': False
        }})

@mod_auth.route('/register/', methods=['GET'])
def register():
    #get params: password:str, fullname:str, b64url:str, description:str
    username = request.args.get('fullname')
    password = request.args.get('password')
    fullname = request.args.get('fullname')
    image = request.args.get('image')
    description = request.args.get('description')

    if User.query.filter_by(username=username).first():
        return resp_handler.get_handler("response_ok", {"data": {
            'status': False
        }})
    else:
        user = User(username=username, password=password, fullname=fullname, image=image, descrpt=description)
        db.session.add(user)
        db.session.commit()
        return resp_handler.get_handler("response_ok", {"data": {
            'status': True
        }})


