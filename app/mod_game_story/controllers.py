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
from app.models.models import User, TruthDareHistory, Story_Object, Story_Context, Story_Conversation

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
mod_game_story = Blueprint('game_story', __name__, url_prefix='/api/v1/games/story')

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2", cache_dir="instance/cache")
tokenizer.save_pretrained("instance/cache")

def calculate_tokens(prompt):
    return len(tokenizer(prompt)["input_ids"])

def generate_prompt(prompt, token_request, stop=False):
    openai.api_key =  ''

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.8,
        max_tokens=token_request,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
        stop=["Bot > ", "Prompt > ", "Anna > ", "Bastien > "] if stop else None,
    )

    response = str(response['choices'][0]['text'])

    response = response.strip(" ")
    response = response.strip("\n")

    return f"{response.strip()}"

def generate_story_context(title, description, theme, location):
    prompt = f"Real Life Context: \nAnna:\n- Young Adult\n- speaks English, Russian and some Irish.\n- likes sewing, listening to Spotify\n- her birthday is June 22nd 2005\n- Wants to take a hairdressing course during the summer, in moldova, that her sister Nia completed.\n- The nickname she gave Bastien is \"Mr. Krabby\".\n- Lovely blond hairs.\n- Objects: Golden earrings (XMas gift from Bastien), Panda stuffed toy (that bastien bought her at IKEA on a date, but she doesn't use it/hold it often).\n\nBastien\n- Young Adult\n- born in France and grew up in Ireland. Speaks french.\n- He enjoys chess, programming, and listening to Spotify with Anna.\n- has few pet names for Anna, like: Smoothie and Sweetie. Bastien has brown hair and eyes.\n- Objects: Chessboard & Book: Odyssey by Homer (Xmas gifts from Anna), and Airpods\n----------------\nIntro: GPT3, you are a professional writer with many years of experience. You are assisting a story telling game. You take a user input, and you turn the user input into an opening passage for a story. You must be as descriptive as possible, to give the highest quality writing/short story. Do not introduce the characters in the opening.\n----------------\nTitle: {title}\nDescription: {description}\nCharacters: Anna & Bastien\nTheme: {theme}\nStarting Location: {location}\n\nStory Opener >"

    print(f'\n\n\t[*] DEBUG | We are using {calculate_tokens(prompt)} tokens\n\n')
    print(f'\n\n\t[*] DEBUG | Generating from prompt: {prompt}\n\n')

    tokens = calculate_tokens(prompt) + 1

    token_request = 4000 - tokens

    return generate_prompt(prompt, token_request)

def generate_story_conversation(story, character, prompt):
    prompt=f"Intro: GPT3, you are a professional writer with many years of experience. You are assisting a story telling game. You take a user input, and you turn the user input into a passage of a story. You must be as descriptive as possible, to give the highest quality writing/short story. Pause the narration where the user's pauses his prompt, and leave the story hanging.\n----------------\nExample:\nIt was a dark and stormy night, and the wind howled through the deserted streets. The only sound that echoed was the tapping of raindrops against the pavement. Bastien had been feeling uneasy all day, and he now walked through the old cemetery in an attempt to clear his head. Wandering through the graveyard, it felt like something was watching him.\nPrompt > [Bastien] [Action] I turn around and check the window. But I find nothing... I go back home. Stop narration when I reach my front door.\nBot > The hair on the back of Bastien's neck stood up and a shiver ran down his spine. He turned around and checked the window. But he found nothing, only the faint reflection of his own fear. He tried to shake it off and continued on his way, but he couldn't shake the feeling that he was being followed. Suddenly, he heard a rustling of leaves behind him, and he spun around. Again, he found nothing, but the unease lingered, and he decided to make his way back home as quickly as he can. He began slowing down as he closed in the distance to the front door.\n----------------\n{story}\nPrompt > [{character}] [Story] {prompt}\nBot >"

    print(f'DEBUG | We are using {calculate_tokens(prompt)} tokens')
    print(f'DEBUG | Generating from prompt: {prompt}')

    tokens = calculate_tokens(prompt) + 1

    token_request = 4000 - tokens

    return generate_prompt(prompt, token_request, stop=True)

@mod_game_story.route('/', methods=['GET', 'POST'])
def list_stories():
    # function to list all stories

    try:
        stories = Story_Object.query.all()
        data = []
        for story in stories:
            data.append({
                'id': story.id,
                'name': story.name,
                'descrpt': story.descrpt,
                'theme': story.theme,
                'id': story.id,
            })
        return resp_handler.get_handler("response_ok", {"data": data})

    except:
        pass

    return resp_handler.get_handler("unhandled_error", "Missing username/secret")

# create new story
@mod_game_story.route('/new/<theme>/<location>/<name>/<description>/', methods=['GET', 'POST'])
def new_story(theme, location, name, description):
    # function to create new story

    # create new story
    new_story = Story_Object(name=name, descrpt=description, theme=theme, location=location)
    db.session.add(new_story)
    db.session.commit()

    # delete all conversations for this story (old records)
    Story_Conversation.query.filter_by(storyID=new_story.id).delete()
    db.session.commit()

    story_conversation = Story_Conversation(
        username="Bot",
        message=generate_story_context(name, description, theme, location),
        storyID=new_story.id
    )
    db.session.add(story_conversation)
    db.session.commit()

    # get all (ws, storyID) in subscriptions, where storyID == storyID
    for ws, _storyID in subscriptions.values():
        if not ws:
            continue
        try:
            ws.send(json.dumps({
                'type': 'new_story',
                'data': {
                    'id': new_story.id,
                    'name': new_story.name,
                    'descrpt': new_story.descrpt,
                    'theme': new_story.theme,
                    'id': new_story.id,
                }
            }))
        except:
            pass



    return resp_handler.get_handler("response_ok", {"data": {
        'id': new_story.id,
        'name': new_story.name,
        'descrpt': new_story.descrpt,
        'theme': new_story.theme,
        'id': new_story.id,
    }})

        
# get story
@mod_game_story.route('/<storyID>/', methods=['GET', 'POST'])
def get_story(storyID):
    # function to get story

    try:
        story = Story_Object.query.filter_by(id=storyID).first()
        data = {
            'id': story.id,
            'name': story.name,
            'descrpt': story.descrpt,
            'theme': story.theme,
            'id': story.id,
        }
        return resp_handler.get_handler("response_ok", {"data": data})

    except:
        pass

    return

@mod_game_story.route('/<storyID>/delete/', methods=['GET', 'POST'])
def delete_story(storyID):
    # function to delete story

    try:
        Story_Object.query.filter_by(id=storyID).delete()
        db.session.commit()
        return resp_handler.get_handler("response_ok", {"data": {}})

    except:
        pass

    return

# get story's context
@mod_game_story.route('/<storyID>/context/', methods=['GET', 'POST'])
def get_story_context(storyID):
    # function to get story's context
    return resp_handler.get_handler("response_ok", {"data": {}})
    try:
        context = Story_Context.query.filter_by(storyID=storyID).first()
        data = {
            'id': context.id,
            'context': context.context,
            'storyID': context.storyID,
        }
        return resp_handler.get_handler("response_ok", {"data": data})

    except:
        pass

    return

# get story's conversation
@mod_game_story.route('/<storyID>/conversations', methods=['GET', 'POST'])
def get_story_conversations(storyID):
    # function to get story's conversation

    try:
        conversations = Story_Conversation.query.filter_by(storyID=storyID).all()
        data = []
        for conv in conversations:
            data.append(
                {'id': conv.id,
                'username': conv.username,
                'message': conv.message,
                'storyID': conv.storyID,
                }
            )
        
        for ws, _storyID in subscriptions.values():
            if not ws:
                continue
            try:
                if _storyID == storyID:
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'get_story_conversations',
                        'message': 'Story conversations',
                        'details': data
                    }))
            except:
                pass
            
        return resp_handler.get_handler("response_ok", {"data": data})
    
    except:
        pass

    return


# Add a new conversation
@mod_game_story.route('/<storyID>/conversations/new', methods=['GET', 'POST'])
def new_story_conversation(storyID, username=None, message=None):
    # function to add a new conversation

    try:
        if username is None:
            username = request.json['username']
        if message is None:
            message = request.json['message']

        # get last message
        last_message = Story_Conversation.query.filter_by(storyID=storyID).all()[-1]
        if (last_message.username != "Bot"):
            return resp_handler.get_handler("response_error", {"data": {}})

        story_conversation = Story_Conversation(
            username=username,
            message=message,
            storyID=storyID
        )
        db.session.add(story_conversation)
        db.session.commit()

        # get all (ws, storyID) in subscriptions, where storyID == storyID
        for ws, _storyID in subscriptions.values():
            if not ws:
                continue
            try:
                if _storyID == storyID:
                    ws.send(json.dumps({
                        'type': 'new_conversation',
                        'status': 0,
                        'data': {
                            'id': story_conversation.id,
                            'username': story_conversation.username,
                            'message': story_conversation.message,
                            'storyID': story_conversation.storyID,
                        }
                    }))
            except:
                pass

        return resp_handler.get_handler("response_ok", {"data": {
            'id': story_conversation.id,
            'username': story_conversation.username,
            'message': story_conversation.message,
            'storyID': story_conversation.storyID,
        }})

    except:
        pass

    return

# Add a new conversation
@mod_game_story.route('/<storyID>/conversations/new/<username>/<message>', methods=['GET', 'POST'])
def new_story_conversation_direct(storyID, username=None, message=None):
    return new_story_conversation(storyID, username, message)

@mod_game_story.route('/<storyID>/conversations/new/BOT', methods=['GET', 'POST'])
def new_story_conversation_bot(storyID):
    # function to add a new conversation

    story = Story_Object.query.filter_by(id=storyID).first()
    if story is None:
        return resp_handler.get_handler("response_error", {"data": {}})

    title = story.name
    description = story.descrpt
    theme = story.theme
    location = story.location

    story_context = f""

    # get all messages from user Bot, to add to the context
    messages = Story_Conversation.query.filter_by(storyID=storyID, username='Bot').all()
    for message in messages:
        story_context += "\n\n" + message.message

    for message in reversed(messages):
        if calculate_tokens(story_context + "\n\n" + message.message) <= 3400:
            story_context = message.message + "\n\n" + story_context
        else:
            break

    story_context = f"Real Life Context: \nAnna:\n- Young Adult\n- speaks English, Russian and some Irish.\n- likes sewing, listening to Spotify\n- her birthday is June 22nd 2005\n- Wants to take a hairdressing course during the summer, in moldova, that her sister Nia completed.\n- The nickname she gave Bastien is \"Mr. Krabby\".\n- Lovely blond hairs.\n- Objects: Golden earrings (XMas gift from Bastien), Panda stuffed toy (that bastien bought her at IKEA on a date, but she doesn't use it/hold it often).\n\nBastien\n- Young Adult\n- born in France and grew up in Ireland. Speaks french.\n- He enjoys chess, programming, and listening to Spotify with Anna.\n- has few pet names for Anna, like: Smoothie and Sweetie. Bastien has brown hair and eyes.\n- Objects: Chessboard & Book: Odyssey by Homer (Xmas gifts from Anna), and Airpods.\n----------------\nIntro: GPT3, you are a professional writer with many years of experience. You are assisting a story telling game. You take a user input, and you turn the user input into a passage of a story. You must be as descriptive as possible, to give the highest quality writing/short story. Pause the narration where the user's pauses his prompt, and leave the story hanging.\n----------------\nExample:\nIt was a dark and stormy night, and the wind howled through the deserted streets. The only sound that echoed was the tapping of raindrops against the pavement. Bastien had been feeling uneasy all day, and he now walked through the old cemetery in an attempt to clear his head. Wandering through the graveyard, it felt like something was watching him.\nPrompt > [Bastien] [Action] I turn around and check the window. But I find nothing... I go back home. Stop narration when I reach my front door.\nBot > The hair on the back of Bastien's neck stood up and a shiver ran down his spine. He turned around and checked the window. But he found nothing, only the faint reflection of his own fear. He tried to shake it off and continued on his way, but he couldn't shake the feeling that he was being followed. Suddenly, he heard a rustling of leaves behind him, and he spun around. Again, he found nothing, but the unease lingered, and he decided to make his way back home as quickly as he can. He began slowing down as he closed in the distance to the front door.\n----------------\nTitle: {title}\nDescription: {description}\nCharacters: Anna & Bastien\nTheme: {theme}\nStarting Location: {location}\n----------------\n{story_context}"

    # get last message
    last_message = Story_Conversation.query.filter_by(storyID=storyID).all()[-1]
    if (last_message.username == "Bot"):
        return resp_handler.get_handler("response_error", {"data": {}})

    story_conversation = Story_Conversation(
        username="Bot",
        message=generate_story_conversation(story_context, last_message.username,last_message.message),
        storyID=storyID
    )
    db.session.add(story_conversation)
    db.session.commit()

    # get all (ws, storyID) in subscriptions, where storyID == storyID
    for ws, _storyID in subscriptions.values():
        if not ws:
            continue
        try:
            if _storyID == storyID:
                ws.send(json.dumps({
                    'type': 'new_conversation',
                    'status': 0,
                    'data': {
                        'id': story_conversation.id,
                        'username': story_conversation.username,
                        'message': story_conversation.message,
                        'storyID': story_conversation.storyID,
                    }
                }))
        except:
            pass

    return resp_handler.get_handler("response_ok", {"data": {
        'id': story_conversation.id,
        'username': story_conversation.username,
        'message': story_conversation.message,
        'storyID': story_conversation.storyID,
    }})


# remove a conversation
@mod_game_story.route('/<storyID>/conversations/remove/index/<convID>', methods=['GET', 'POST'])
def remove_story_conversation(storyID, convID):
    # function to remove a conversation

    try:
        # don't remove if last message is also the first message
        if convID == 1:
            return resp_handler.get_handler("response_error", {"data": {}})

        Story_Conversation.query.filter_by(id=convID).delete()
        db.session.commit()

        # get all (ws, storyID) in subscriptions, where storyID == storyID
        for ws, _storyID in subscriptions.values():
            if not ws:
                continue
            try:
                print('going to try to send remove_conversation callback')
                if _storyID == storyID:
                    print('will send remove_conversation callback')
                    ws.send(json.dumps({
                        'type': 'remove_conversation',
                        'status': 0,
                        'data': {
                            'id': convID,
                            'status': 'deleted'
                        }
                    }))
                    print('sent remove_conversation callback')
                else:
                    print('will not send remove_conversation callback')
            except:
                pass


        return resp_handler.get_handler("response_ok", {"data": {
            'id': convID,
            'status': 'deleted'
        }})

    except Exception as e:
        print(e)

    return

# remove last conversation
@mod_game_story.route('/<storyID>/conversations/remove/last', methods=['GET', 'POST'])
def remove_story_last_conversation(storyID):
    # function to remove last conversation

    try:
        last_conv = Story_Conversation.query.filter_by(storyID=storyID).order_by(Story_Conversation.id.desc()).first()
        
        # don't remove if last message is also the first message
        if last_conv.id == 1:
            return resp_handler.get_handler("response_error", {"data": {}})

        Story_Conversation.query.filter_by(id=last_conv.id).delete()
        db.session.commit()

        # get all (ws, storyID) in subscriptions, where storyID == storyID
        for ws, _storyID in subscriptions.values():
            if not ws:
                continue
            try:
                ws.send(json.dumps({
                    'type': 'remove_last_conversation',
                    'data': {
                        'id': last_conv.id,
                        'status': 'deleted'
                    }
                }))
            except:
                pass
        
        # refresh message list, by calling get_story_conversations
        get_story_conversations(storyID)

        return resp_handler.get_handler("response_ok", {"data": {
            'id': last_conv.id,
            'status': 'deleted'
        }})

    except:
        pass

    return

# get full context with all messages
@mod_game_story.route('/<storyID>/context/full', methods=['GET', 'POST'])
def get_story_full_context(storyID):
    # function to get full context
    return resp_handler.get_handler("response_ok", {"data": {   }})

    try:
        context = Story_Context.query.filter_by(storyID=storyID).first().context

        # get all messages to add to the context
        messages = Story_Conversation.query.filter_by(storyID=storyID).all()
        for message in messages:
            context += f'{message.username} > {message.message}\n'

        return resp_handler.get_handler("response_ok", {"data": {
            'context': context
        }})

    except:
        pass

    return

subscriptions = {
    # username: (ws, storyID)
}

# WS route for all of these functions/route above.
@sock.route('/api/v1/games/story/ws')
def endpoint_mngr_story(ws):
    try:
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
                    subscriptions[username] = (ws, args['storyID'])
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

                elif action == 'list_stories':
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'list_stories',
                        'message': 'List of stories',
                        'details': json.loads(list_stories()[0])
                    }))
                elif action == 'new_story':
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'new_story',
                        'message': 'New story created',
                        'details': json.loads(new_story(args['theme'], args['location'], args['name'], args['description'])[0])
                    }))
                elif action == 'get_story':
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'get_story',
                        'message': 'Story data',
                        'details': json.loads(get_story(args['storyID'])[0])
                    }))
                elif action == 'get_story_context':
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'get_story_context',
                        'message': 'Story context',
                        'details': json.loads(get_story_context(args['storyID'])[0])
                    }))
                elif action == 'get_story_conversations':
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'get_story_conversations',
                        'message': 'Story conversations',
                        'details': json.loads(get_story_conversations(args['storyID'])[0])
                    }))
                elif action == 'new_story_conversation':
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'new_story_conversation',
                        'message': 'New conversation created',
                        'details': json.loads(new_story_conversation(args['storyID'], args['username'], args['message'])[0])
                    }))
                elif action == 'new_story_conversation_direct':
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'new_story_conversation_direct',
                        'message': 'New conversation created',
                        'details': json.loads(new_story_conversation_direct(args['storyID'], args['username'], args['message'])[0])
                    }))
                elif action == 'new_story_conversation_bot':
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'new_story_conversation_bot',
                        'message': 'New conversation created',
                        'details': json.loads(new_story_conversation_bot(args['storyID'])[0])
                    }))
                elif action == 'remove_story_conversation':
                    try:
                        ws.send(json.dumps({
                            'status': 0,
                            'type': 'remove_story_conversation',
                            'message': 'Conversation removed',
                            'details': json.loads(remove_story_conversation(args['storyID'], args['convID'])[0])
                        }))
                    except:
                        ws.send(json.dumps({
                            'status': 0,
                            'type': 'remove_story_conversation',
                            'message': 'Conversation removed',
                            'details': -1
                        }))
                elif action == 'remove_story_last_conversation':
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'remove_story_last_conversation',
                        'message': 'Last conversation removed',
                        'details': json.loads(remove_story_last_conversation(args['storyID'])[0])
                    }))
                elif action == 'get_story_full_context':
                    ws.send(json.dumps({
                        'status': 0,
                        'type': 'get_story_full_context',
                        'message': 'Full context',
                        'details': json.loads(get_story_full_context(args['storyID'])[0])
                    }))
                else:
                    ws.send(json.dumps({
                        'status': 1,
                        'type': 'error',
                        'message': 'Invalid request',
                        'details': 'Invalid action'
                    }))
    except Exception as e:
        print(e)

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
// Args: storyID

// Action: ack
// Args: None

// Action: list_stories
// Args: None

// Action: new_story
// Args: theme, location, name, description

// Action: get_story
// Args: storyID

// Action: get_story_context
// Args: storyID

// Action: get_story_conversations
// Args: storyID

// Action: new_story_conversation
// Args: storyID, username, message

// Action: new_story_conversation_direct
// Args: storyID, username, message

// Action: new_story_conversation_bot
// Args: storyID

// Action: remove_story_conversation
// Args: storyID, convID

// Action: remove_story_last_conversation
// Args: storyID

// Action: get_story_full_context
// Args: storyID

// Incoming Subscription Message:

// Type: new_conversation
// data: { 'storyID': storyID, 'id': convID, 'username': username, 'message': message }
'''
