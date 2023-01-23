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
from app.mod_dates.forms import LoginForm, RegisterForm, VerifyForm

# Import module models (i.e. User)
from app.models.models import User

from app import resp_handler

from typing import List, Tuple

import secrets

import json

import re


# Define the blueprint: 'dates', set its url prefix: app.url/dates
mod_dates = Blueprint('dates', __name__, url_prefix='/api/v1/dates')


@mod_dates.route('/', methods=['GET', 'POST'])
def list():
    # function to list all user's dates (with its partner)

    try:
        #auth = request.headers.get('Authorization')
        #username,token = pry_authorization(auth)

        #status, user = verify_token(username,token)
        status = True # dummy data (mockup) for now

        if status:
            # dummy data (mockup) for now
            data = [
                {
                    "id": 1,
                    "title": "IKEA Trip",
                    "completed": False,
                    "pending": True,
                    "partner": "Smoothie",
                    "photo": "https://www.finished.ie/wp-content/uploads/2018/01/ikea-logo.jpg",
                    "icon": "https://www.finished.ie/wp-content/uploads/2018/01/ikea-logo.jpg",
                    "timestamp": "2023-01-27T09:00:00.000Z",
                    "location": "IKEA - Dublin 15",
                    "description": "We will go to IKEA ;)",
                    "status": "pending",
                    "approved": False,
                    "rejected": False,
                    "approved_timestamp": None,    
                },
                {
                    "id": 2,
                    "title": "Bowling",
                    "completed": False,
                    "pending": True,
                    "partner": "Smoothie",
                    "photo": "https://img.goldenpages.ie/3313541.png",
                    "icon": "https://img.goldenpages.ie/3313541.png",
                    "timestamp": "2023-02-03T010:30:00.000Z",
                    "location": "BrayBowling, Bray, Co. Wicklow",
                    "description": "We will bowl together and have fun with the arcades :D",
                    "status": "pending",
                    "approved": False,
                    "rejected": False,
                    "approved_timestamp": None,
                }
            ]

            return resp_handler.get_handler("response_ok", {"data": data})
        return resp_handler.get_handler("token_auth")
    except:
        pass

    return resp_handler.get_handler("unhandled_error", "Missing username/secret")

