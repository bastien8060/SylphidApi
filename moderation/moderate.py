# python program 
# task: download url (https://raw.githubusercontent.com/sylhare/Truth-or-Dare/master/src/output.json)
# parse json
# register keyboard events
# loop through json
#    update screen with card
#    in press function, check if key is space or not. Match current keypress to current card.
#        if space, pass
#        if anything else, add ID to list of banned IDs
#    clear screen
# loop finished
# print out list of banned IDs
# pickle.dump({'banned': banned,'last_card': current['id']}, f)

# at any point, if the user presses ctrl+c, the program should exit and print out the list of banned IDs

# format of item: [{"id": "1", "level": "2", "summary": "I dare you to do 10 pushups with one hand in less than a minute", "time": "60", "turns": "", "type": "Dare"}, {"id": "2", "level": "2", "summary": "What actor/actress do you prefer?", "time": "", "turns": "", "type": "Truth"},...]

import json
import os
import requests
import sys
import time
from sshkeyboard import listen_keyboard, stop_listening
import pickle

resp = requests.get('https://raw.githubusercontent.com/sylhare/Truth-or-Dare/master/src/output.json')
data = resp.json()

banned = []
current = {}
last_card = 0

# restore pickle (banned and last_card)
try:
    with open('moderation.pickle', 'rb') as f:
        p_data = pickle.load(f)
        banned = p_data['banned']
        last_card = int(p_data['last_card'])
    print(f"Restored banned: {banned} and last_card: {last_card}")
except Exception as e:
    print(e)

def press(key):
    global banned
    global data
    global current
    if key == "space":
        print("pass")
    else:
        print("banned")
        banned.append(int(current['id']))
    stop_listening()
    return False

try:
    while True:
        for item in data:
            if int(item['id']) in banned or int(item['id']) < int(last_card):
                continue
            os.system('cls' if os.name == 'nt' else 'clear')
            current = item
            percentage = f"{int(current['id']) / int(data[-1]['id']) * 100:.2f}%"
            print(f"[{item['id']} / {percentage}]\t{item['summary']}")
            listen_keyboard(
                on_press=press,
            )
            last_card = int(item['id'])
except KeyboardInterrupt:
    print(banned)
    with open('moderation.pickle', 'wb') as f:
        pickle.dump({
            'banned': banned,
            'last_card': current['id']
        }, f)

# save as JSON
with open('moderation.json', 'w') as f:
    json.dump({'banned': banned,
                'last_card_processed': current['id'],
                'last_card': data[-1]['id'],
                'total_cards': len(data),
                'new_total_cards': len(data) - len(banned),
                'progress_%': f"{int(current['id']) / int(data[-1]['id']) * 100:.2f}%"}, f)




