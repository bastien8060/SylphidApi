# python program 
# task: download url (https://raw.githubusercontent.com/sylhare/Truth-or-Dare/master/src/output.json)
# parse json
# loop through json
#    record card type (truth, dare, etc..) tallybar
# Display frequency of each card type

import json
import os
import requests

resp = requests.get('https://raw.githubusercontent.com/sylhare/Truth-or-Dare/master/src/output.json')
data = resp.json()

tally = {}

for item in data:
    if item['type'] not in tally:
        tally[item['type']] = 0
    tally[item['type']] += 1

print(tally)

