# Import flask dependencies
import json
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
from app.models.models import User, Status

from app import resp_handler

from typing import List, Tuple

import secrets

import datetime

from multiprocessing import Process

import time

from app import sock


# Define the blueprint: 'dates', set its url prefix: app.url/dates
mod_config = Blueprint('config', __name__, url_prefix='/api/v1/config')

configs = {
    'touchDuration': 1500,
    'games_enabled': [1, 2, 3, 4, 5, 6],
}

@mod_config.route('/get', methods=['GET'])
def list_others_status():
    # function to check a user's status
    try:
        return resp_handler.get_handler("response_ok", {"data": 
            {
                'status': 0,
                'configs': configs,
            }
        })
    except:
        pass

    return resp_handler.get_handler("unhandled_error", "Missing username/secret")

