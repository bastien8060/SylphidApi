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
mod_updates = Blueprint('updates', __name__, url_prefix='/api/v1/updates')


@mod_updates.route('/', methods=['GET', 'POST'])
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
                    "subtitle": "Game Progress",
                    "title": "Dungeon and Dragons",
                    "description": "Smoothie has made progress in Dungeon and Dragons while you were away.",
                    "from": "Smoothie",
                    "isMediaCard": False,
                    "timestamp": "2023-01-15T20:34:00.000Z",
                },
                {
                    "id": 2,
                    "subtitle": "New Serie Recommendation",
                    "title": "Arcane - Season 1",
                    "description": "Smoothie has recommended you to watch Arcane - Season 1. You should check it out!",
                    "from": "Smoothie",
                    "isMediaCard": True,
                    "timestamp": "2023-01-15T20:37:00.000Z",
                    "media": {
                        "title": "Arcane - Season 1",
                        "description": "I think you should watch this serie. It's really good! :)",
                        "image": "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt8739d07baed7d77d/5ed9b1c197379739c07664d9/Arcane_Announcement_Banner.jpg",
                        "url": "https://www.imdb.com/title/tt11126994"
                    }

                }
            ]#avatar last airbender is a good show btw :D

            return resp_handler.get_handler("response_ok", {"data": data})
        return resp_handler.get_handler("token_auth")
    except:
        pass

    return resp_handler.get_handler("unhandled_error", "Missing username/secret")

