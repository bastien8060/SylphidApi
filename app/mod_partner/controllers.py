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
from app.models.models import User, Status

from app import resp_handler

from typing import List, Tuple

import secrets

import datetime

from multiprocessing import Process

import time


# Define the blueprint: 'dates', set its url prefix: app.url/dates
mod_partner = Blueprint('partner', __name__, url_prefix='/api/v1/partner')

partners = ['Smoothie', 'Krabby']
partners_img = {
    'Smoothie': '/assets/11.jpg',
    'Krabby': '/assets/10.jpg'
}

process = None



def set_partners_live_status(status: List[dict]):
    #set back to Status table
    for username in status:
        item = status[username]
        if Status.query.filter_by(username=username).first():
            user_status = Status.query.filter_by(username=username).first()
            user_status.online = item['online']
            user_status.last_seen = item['last_seen']
            user_status.page = item['page']
            #db.session.commit()
        else:
            user_status = Status(username=username, online=item['online'], last_seen=item['last_seen'], page=item['page'])
            db.session.add(user_status)
            #db.session.commit()
    db.session.commit()

def get_partners_live_status():
    #turn back to dict[username] = {online, last_seen, page}
    status = Status.query.all()
    status_dict = {}
    for item in status:
        status_dict[item.username] = {
            'online': item.online,
            'last_seen': item.last_seen,
            'page': item.page
        }
    return status_dict


def clearStatusThread():
    while True:
        partners_live_status = get_partners_live_status()

        for partner in partners:
            new_status = partners_live_status[partner]
            new_status['online'] = False
            partners_live_status[partner] = new_status
            print('cleared status')

        set_partners_live_status(partners_live_status)

        time.sleep(90)

def clearStatusThreadManager():
    global process

    if process is None:
        print('starting thread')
        process = Process(target=clearStatusThread)
        process.start()



    



@mod_partner.route('/<string:partner>/status/set/<string:page>', methods=['GET'])
def set_status(partner, page):
    # function to set a user's status to online and set the last seen page

    if partner not in partners:
        return resp_handler.get_handler("token_auth")

    partners_live_status = get_partners_live_status()

    partners_live_status[partner] = {
        'online': True,
        'last_seen': datetime.datetime.now(),
        'page': page,
        'username': partner
    }

    set_partners_live_status(partners_live_status)

    return resp_handler.get_handler("response_ok", {"data": {
        'status': True
    }})


    return resp_handler.get_handler("unhandled_error", "Missing username/secret")


@mod_partner.route('/<string:partner>/other_status', methods=['GET'])
def list(partner):
    # function to check a user's status

    try:
        clearStatusThreadManager()

        if partner not in partners:
            return resp_handler.get_handler("token_auth")

        other_partner = partners[0] if partner == partners[1] else partners[1]

        partners_live_status = get_partners_live_status()

        if other_partner not in partners_live_status:
            return resp_handler.get_handler("response_ok", {"data": {
                'status': {
                    'online': False,
                    'last_seen': None,
                    'page': None,
                    'name': other_partner,
                    'img': partners_img[other_partner]
                }
            }})

        data = partners_live_status[other_partner]

        data['name'] = other_partner
        data['img'] = partners_img[other_partner]

        return resp_handler.get_handler("response_ok", {"data": data})    
        
    except:
        pass

    return resp_handler.get_handler("unhandled_error", "Missing username/secret")

