# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from sqlalchemy import or_
from unidecode import unidecode

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module models (i.e. User)
from app.models.models import User, TruthDareHistory, DnD_Campaign, DnD_Context, DnD_Conversation

from app import resp_handler

from typing import List, Tuple

import datetime

import secrets

import json

import re

import requests

import openai

from transformers import GPT2TokenizerFast

from app import sock

# Define the blueprint: 'dates', set its url prefix: app.url/dates
mod_game_dnd = Blueprint('game_dnd', __name__, url_prefix='/api/v1/games/dnd')

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2", cache_dir="instance/cache")
tokenizer.save_pretrained("instance/cache")

def calculate_tokens(prompt):
    return len(tokenizer(prompt)["input_ids"])

def generate_message(prompt, user=None, newline=False):
    openai.api_key =  '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'

    if not (user is None):
        prompt += f"{user} > "
    
    if newline:
        prompt += "\n"

    print(f'DEBUG | We are using {calculate_tokens(prompt)} tokens')
    print(f'DEBUG | Generating from prompt: {prompt}')

    tokens = calculate_tokens(prompt) + 1

    token_request = 4000 - tokens

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.8,
        max_tokens=token_request,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
        stop=["Anna >", "Bastien >"]
    )

    return f"{user} > {str(response['choices'][0]['text']).strip()}"

@mod_game_dnd.route('/', methods=['GET', 'POST'])
def list_campaigns():
    # function to list all campaigns

    try:
        DnD_Campaigns = DnD_Campaign.query.all()
        data = []
        for campaign in DnD_Campaigns:
            data.append({
                'id': campaign.id,
                'name': campaign.name,
                'descrpt': campaign.descrpt,
                'theme': campaign.theme,
                'id': campaign.id,
            })
        return resp_handler.get_handler("response_ok", {"data": data})

    except:
        pass

    return resp_handler.get_handler("unhandled_error", "Missing username/secret")

# create new campaign
@mod_game_dnd.route('/new/<theme>/<location>/<name>/<description>/', methods=['GET', 'POST'])
def new_campaign(theme, location, name, description):
    # function to create new campaign

    # create new campaign
    new_campaign = DnD_Campaign(name=name, descrpt=description, theme=theme, location=location)
    db.session.add(new_campaign)
    db.session.commit()

    timestamp = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    context = f"Intro: GPT3, you are the DM. You will play a campaign of DnD\n----------------\nDnD - for DM to remember in game | [remember]: \n-- player1 is Anna; player2 is Bastien\n----------------\nDnD Real Life Context: \n\n- Anna, 17, is Irish but born in Moldova. She speaks English, Russian and some Irish. Lives in Ashbourne, Meath, with her mother who is strict, father who is nicer. 2 sisters: Daria (15yo), who studies her Leaving cert (Institute of Education, Dublin). Also Nia (23yo) who study Radiology at UCD and. Anna studies Midwifery at UCD and takes the 103/103x bus from Ashbourne to Dublin and the 46a/145/155/39a from Dublin to UCD. She likes sewing, listening to Spotify, her birthday is June 22nd 2005, wants to visit Moldova next summer with her partner Bastien, meet her grandparents, take a hairdressing course her sister Nia completed. Anna has nicknames for Bastien \"Pumpkin, Mr. Krabby, handsome\", likes receiving Shein bags or wine from NPCs in DnD campaigns. Likes hitting Bastien with a baguette. Her father's name is Yuri, her best friend is a Portuguese girl, Livia (23), who is sarcastic and has dark humor.\n- Emily: 19, Australian studying CompSci in Dublin, dark humor, often at Starbucks\n- Iakov or Yasha: Russian, fascinated by cars and car-racing. Goes swimming in UCD.\n- Bastien, 18 and from Stillorgan, was born in France and grew up in Ireland. He's been in a relationship with Anna since September 9th, 2022. He has two brothers, Louis (8) and Arthur (1). His father is strict but his mother is nicer. He enjoys chess, programming, and listening to Spotify with Anna. He often visits Anna at UCD and plans to study Computer Science there next year. He walks Anna to her bus stop after taking the 39a from UCD to the city center and calls her by various pet names (Smoothie, Sweetie, Cutie pie, sweetheart, darling). Bastien is 5ft 8, has brown hair and eyes. He's visited Anna in Barcelona. Bastien's birthday is the 20th April 2004\n- Jacky: Chinese, loves CompSci, building keyboards, Minecraft, anime/mangas, and fountain pens\n- Daria doesn't really like Anna and Bastien's friends: Jacky, Emily, Iakov, etc.. Daria is quite shy and doesn't talk much. Nia: very talktative\n----------------\nDnD Params:\nCurrent timestamp: {timestamp}\nTheme: {theme}\nStarting point: {location}\n----------------\nInstructions for DM:\n-- Should initiate actions from NPCs. Eg: attack, talk, be kind, etc...\n-- Should create long prompts/responses to the users, describe clearly what happened, create plot twists, etc...\n-- Should describe surroundings.\n-- NPCs should interact with players\n-- DM can ask dice rolls for the story.\n-- NPCs should be reffered to with a name or description.\n-- DO not describe or introduce too many friends.\n-- DM should start with [remember] all important details to be remembered, eg. ```\nDM> [remember] fact 1, fact2\nDM> Okayy you are now in fact1, and fact2 has...\n```\n----------------\nDM > [remember] player1 is Anna; player2 is Bastien\nDM > We have two players! Anna and Bastien!\nBastien > Are you ready Anna?\nAnna > Yes!\nBastien > Great! You may begin game master! Create some NPCs, tell us where we are and start the game!\n"

    dnd_context = DnD_Context(
        int(new_campaign.id),
        context=context,
    )
    db.session.add(dnd_context)
    db.session.commit()

    dnd_conversation = DnD_Conversation(
        username="DM",
        message=generate_message(context, 'DM', newline=True),
        campaignID=new_campaign.id
    )
    db.session.add(dnd_conversation)
    db.session.commit()

    # get all (ws, campaignID) in subscriptions, where campaignID == campaignID
    for ws, _campaignID in subscriptions.values():
        ws.send(json.dumps({
            'type': 'new_campaign',
            'data': {
                'id': new_campaign.id,
                'name': new_campaign.name,
                'descrpt': new_campaign.descrpt,
                'theme': new_campaign.theme,
                'id': new_campaign.id,
            }
        }))



    return resp_handler.get_handler("response_ok", {"data": {
        'id': new_campaign.id,
        'name': new_campaign.name,
        'descrpt': new_campaign.descrpt,
        'theme': new_campaign.theme,
        'id': new_campaign.id,
    }})

        
# get campaign
@mod_game_dnd.route('/<campaignID>/', methods=['GET', 'POST'])
def get_campaign(campaignID):
    # function to get campaign

    try:
        campaign = DnD_Campaign.query.filter_by(id=campaignID).first()
        data = {
            'id': campaign.id,
            'name': campaign.name,
            'descrpt': campaign.descrpt,
            'theme': campaign.theme,
            'id': campaign.id,
        }
        return resp_handler.get_handler("response_ok", {"data": data})

    except:
        pass

    return

# get campaign's context
@mod_game_dnd.route('/<campaignID>/context/', methods=['GET', 'POST'])
def get_campaign_context(campaignID):
    # function to get campaign's context

    try:
        context = DnD_Context.query.filter_by(campaignID=campaignID).first()
        data = {
            'id': context.id,
            'context': context.context,
            'campaignID': context.campaignID,
        }
        return resp_handler.get_handler("response_ok", {"data": data})

    except:
        pass

    return

# get campaign's conversation
@mod_game_dnd.route('/<campaignID>/conversations', methods=['GET', 'POST'])
def get_campaign_conversations(campaignID):
    # function to get campaign's conversation

    try:
        conversations = DnD_Conversation.query.filter_by(campaignID=campaignID).all()
        data = []
        for conv in conversations:
            data.append(
                {'id': conv.id,
                'username': conv.username,
                'message': conv.message,
                'campaignID': conv.campaignID,
                }
            )
            
        return resp_handler.get_handler("response_ok", {"data": data})
    
    except:
        pass

    return


# Add a new conversation
@mod_game_dnd.route('/<campaignID>/conversations/new', methods=['GET', 'POST'])
def new_campaign_conversation(campaignID, username=None, message=None):
    # function to add a new conversation

    try:
        if username is None:
            username = request.json['username']
        if message is None:
            message = request.json['message']

        message = f'{username} > {message}'

        dnd_conversation = DnD_Conversation(
            username=username,
            message=message,
            campaignID=campaignID
        )
        db.session.add(dnd_conversation)
        db.session.commit()

        # get all (ws, campaignID) in subscriptions, where campaignID == campaignID
        for ws, _campaignID in subscriptions.values():
            if _campaignID == campaignID:
                ws.send(json.dumps({
                    'type': 'new_conversation',
                    'data': {
                        'id': dnd_conversation.id,
                        'username': dnd_conversation.username,
                        'message': dnd_conversation.message,
                        'campaignID': dnd_conversation.campaignID,
                    }
                }))

        return resp_handler.get_handler("response_ok", {"data": {
            'id': dnd_conversation.id,
            'username': dnd_conversation.username,
            'message': dnd_conversation.message,
            'campaignID': dnd_conversation.campaignID,
        }})

    except:
        pass

    return

# Add a new conversation
@mod_game_dnd.route('/<campaignID>/conversations/new/<username>/<message>', methods=['GET', 'POST'])
def new_campaign_conversation_direct(campaignID, username=None, message=None):
    return new_campaign_conversation(campaignID, username, message)

@mod_game_dnd.route('/<campaignID>/conversations/new/DM', methods=['GET', 'POST'])
def new_campaign_conversation_dm(campaignID):
    # function to add a new conversation

    try:
        context = DnD_Context.query.filter_by(campaignID=campaignID).first().context

        # get all messages to add to the context
        messages = DnD_Conversation.query.filter_by(campaignID=campaignID).all()
        for message in messages:
            context += f'{message.message}\n'

        dnd_conversation = DnD_Conversation(
            username="DM",
            message=generate_message(context, 'DM', newline=True),
            campaignID=campaignID
        )
        db.session.add(dnd_conversation)
        db.session.commit()

        # get all (ws, campaignID) in subscriptions, where campaignID == campaignID
        for ws, _campaignID in subscriptions.values():
            if _campaignID == campaignID:
                ws.send(json.dumps({
                    'type': 'new_conversation',
                    'data': {
                        'id': dnd_conversation.id,
                        'username': dnd_conversation.username,
                        'message': dnd_conversation.message,
                        'campaignID': dnd_conversation.campaignID,
                    }
                }))

        return resp_handler.get_handler("response_ok", {"data": {
            'id': dnd_conversation.id,
            'username': dnd_conversation.username,
            'message': dnd_conversation.message,
            'campaignID': dnd_conversation.campaignID,
        }})
    
    except:
        pass

    return

# remove a conversation
@mod_game_dnd.route('/<campaignID>/conversations/remove/index/<convID>', methods=['GET', 'POST'])
def remove_campaign_conversation(campaignID, convID):
    # function to remove a conversation

    try:
        DnD_Conversation.query.filter_by(id=convID).delete()
        db.session.commit()

        # get all (ws, campaignID) in subscriptions, where campaignID == campaignID
        for ws, _campaignID in subscriptions.values():
            if _campaignID == campaignID:
                ws.send(json.dumps({
                    'type': 'remove_conversation',
                    'data': {
                        'id': convID,
                        'status': 'deleted'
                    }
                }))


        return resp_handler.get_handler("response_ok", {"data": {
            'id': convID,
            'status': 'deleted'
        }})

    except:
        pass

    return

# remove last conversation
@mod_game_dnd.route('/<campaignID>/conversations/remove/last', methods=['GET', 'POST'])
def remove_campaign_last_conversation(campaignID):
    # function to remove last conversation

    try:
        last_conv = DnD_Conversation.query.filter_by(campaignID=campaignID).order_by(DnD_Conversation.id.desc()).first()
        DnD_Conversation.query.filter_by(id=last_conv.id).delete()
        db.session.commit()

        # get all (ws, campaignID) in subscriptions, where campaignID == campaignID
        for ws, _campaignID in subscriptions.values():
            if _campaignID == campaignID:
                ws.send(json.dumps({
                    'type': 'remove_last_conversation',
                    'data': {
                        'id': last_conv.id,
                        'status': 'deleted'
                    }
                }))

        return resp_handler.get_handler("response_ok", {"data": {
            'id': last_conv.id,
            'status': 'deleted'
        }})

    except:
        pass

    return

# get full context with all messages
@mod_game_dnd.route('/<campaignID>/context/full', methods=['GET', 'POST'])
def get_campaign_full_context(campaignID):
    # function to get full context

    try:
        context = DnD_Context.query.filter_by(campaignID=campaignID).first().context

        # get all messages to add to the context
        messages = DnD_Conversation.query.filter_by(campaignID=campaignID).all()
        for message in messages:
            context += f'{message.message}\n'

        return resp_handler.get_handler("response_ok", {"data": {
            'context': context
        }})

    except:
        pass

    return

subscriptions = {
    # username: (ws, campaignID)
}

# WS route for all of these functions/route above.
@sock.route('/api/v1/games/dnd/ws')
def endpoint(ws):
    username = None
    while True:
        # get message from client
        message = ws.receive()

        # Parse the api request
        try:
            req = json.loads(message)
            action = req['action']
            args = req['args']
        except:
            ws.send(json.dumps({
                'status': 1,
                'type': 'error',
                'message': 'Invalid request',
                'details': 'Parsing error'
            }))

        if message is not None:
            if action == 'init':
                username = args['username']
                subscriptions[username] = (ws, -1)
                ws.send(json.dumps({
                    'type': 'init',
                    'status': 0,
                    'message': 'Syn',
                }))
            
            elif action == 'subscribe':
                subscriptions[username] = (ws, args['campaignID'])
                ws.send(json.dumps({
                    'type': 'subscribe',
                    'status': 0,
                    'message': 'Syn',
                }))

            elif action == 'ack':
                ws.send(json.dumps({
                    'type': 'ack',
                    'status': 0,
                    'message': 'Syn',
                }))

            elif action == 'list_campaigns':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'list_campaigns',
                    'message': 'List of campaigns',
                    'details': json.loads(list_campaigns()[0])
                }))
            elif action == 'new_campaign':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'new_campaign',
                    'message': 'New campaign created',
                    'details': json.loads(new_campaign(args['theme'], args['location'], args['name'], args['description'])[0])
                }))
            elif action == 'get_campaign':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'get_campaign',
                    'message': 'Campaign data',
                    'details': json.loads(get_campaign(args['campaignID'])[0])
                }))
            elif action == 'get_campaign_context':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'get_campaign_context',
                    'message': 'Campaign context',
                    'details': json.loads(get_campaign_context(args['campaignID'])[0])
                }))
            elif action == 'get_campaign_conversations':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'get_campaign_conversations',
                    'message': 'Campaign conversations',
                    'details': json.loads(get_campaign_conversations(args['campaignID'])[0])
                }))
            elif action == 'new_campaign_conversation':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'new_campaign_conversation',
                    'message': 'New conversation created',
                    'details': json.loads(new_campaign_conversation(args['campaignID'], args['username'], args['message'])[0])
                }))
            elif action == 'new_campaign_conversation_direct':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'new_campaign_conversation_direct',
                    'message': 'New conversation created',
                    'details': json.loads(new_campaign_conversation_direct(args['campaignID'], args['username'], args['message'])[0])
                }))
            elif action == 'new_campaign_conversation_dm':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'new_campaign_conversation_dm',
                    'message': 'New conversation created',
                    'details': json.loads(new_campaign_conversation_dm(args['campaignID'])[0])
                }))
            elif action == 'remove_campaign_conversation':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'remove_campaign_conversation',
                    'message': 'Conversation removed',
                    'details': json.loads(remove_campaign_conversation(args['campaignID'], args['convID'])[0])
                }))
            elif action == 'remove_campaign_last_conversation':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'remove_campaign_last_conversation',
                    'message': 'Last conversation removed',
                    'details': json.loads(remove_campaign_last_conversation(args['campaignID'])[0])
                }))
            elif action == 'get_campaign_full_context':
                ws.send(json.dumps({
                    'status': 0,
                    'type': 'get_campaign_full_context',
                    'message': 'Full context',
                    'details': json.loads(get_campaign_full_context(args['campaignID'])[0])
                }))
            else:
                ws.send(json.dumps({
                    'status': 1,
                    'type': 'error',
                    'message': 'Invalid request',
                    'details': 'Invalid action'
                }))

'''
// JSON API Map with args for WS API:
// {
//     'action': 'action_name',
//     'args': {
//         'arg1': 'value1',
//         'arg2': 'value2',
//         ...
//     }
// }

// WS API Map Result:
// {
//     'status': 0,
//     'type': 'action_name',
//     'message': 'Message',
//     'details': 'Details/Data'
// }

// WS API Map Error:
// {
//     'status': 1,
//     'type': 'error',
//     'message': 'Error message',
//     'details': 'Error details'
// }

// Action: init
// Args: username

// Action: subscribe
// Args: campaignID

// Action: ack
// Args: None

// Action: list_campaigns
// Args: None

// Action: new_campaign
// Args: theme, location, name, description

// Action: get_campaign
// Args: campaignID

// Action: get_campaign_context
// Args: campaignID

// Action: get_campaign_conversations
// Args: campaignID

// Action: new_campaign_conversation
// Args: campaignID, username, message

// Action: new_campaign_conversation_direct
// Args: campaignID, username, message

// Action: new_campaign_conversation_dm
// Args: campaignID

// Action: remove_campaign_conversation
// Args: campaignID, convID

// Action: remove_campaign_last_conversation
// Args: campaignID

// Action: get_campaign_full_context
// Args: campaignID

// Incoming Subscription Message:

// Type: new_conversation
// data: { 'campaignID': campaignID, 'id': convID, 'username': username, 'message': message }
'''
