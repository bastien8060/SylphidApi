import requests as __requests

__ban_list = {"banned": [3, 45, 85, 86, 87, 89, 93, 97, 99, 102, 103, 104, 105, 106, 107, 108, 120, 136, 144, 147, 154, 155, 243, 244, 246, 247, 250, 252, 253, 254, 255, 256, 257, 261, 262, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 278, 279, 301, 302, 304, 305, 312, 315, 319, 320, 321, 385, 390, 392, 393, 397, 399, 405, 424, 427, 428, 444, 463, 467, 474, 480, 484, 507, 509, 510, 511, 514], "last_card_processed": "553", "last_card": "553", "total_cards": 554, "new_total_cards": 475, "progress_%": "100.00%"}

__resp = __requests.get('https://raw.githubusercontent.com/sylhare/Truth-or-Dare/master/src/output.json')
__data = __resp.json()


# truth or dare
truth_dare = [item for item in __data if int(item['id']) not in __ban_list['banned']]
truth = [item for item in truth_dare if item['type'] == 'Truth']
dare = [item for item in truth_dare if item['type'] == 'Dare']

# conversation starters
truth_topic = [{'summary': item['summary'], 'id': item['id'], "topic_str":"truth", "topic":4} for item in truth]
sexy_topic = [{'summary': item['summary'], 'id': item['id'], "topic_str":"sexy", "topic":0} for item in truth if item['level'] == '5']
casual_topic = [{'summary': item['summary'], 'id': item['id'], "topic_str":"casual", "topic":1} for item in truth if item['level'] == '0' or item['level'] == '1']
topics = [
    {"summary": "What is your favorite color?", "topic_str":"casual", "topic":1, "id": 1},
    {"summary": "What is your favorite food?", "topic_str":"casual", "topic":1, "id": 2},
    {"summary": "What is your favorite movie?", "topic_str":"casual", "topic":1, "id": 3},
    {"summary": "What is your favorite TV show?", "topic_str":"casual", "topic":1, "id": 13},
    {"summary": "What is the most adventurous food you've ever tried?", "topic_str":"casual", "topic":1, "id": 14},
    {"summary": "What is your favorite music genre?", "topic_str":"casual", "topic":1, "id": 15},

    # topic romantic
    {"summary": "What is thing about me?", "topic_str":"romantic", "topic":3, "id": 4},
    {"summary": "What is your favorite memory of us?", "topic_str":"romantic", "topic":3, "id": 5},
    {"summary": "What is your favorite thing about me?", "topic_str":"romantic", "topic":3, "id": 6},
    {"summary": "What is your favorite thing about us?", "topic_str":"romantic", "topic":3, "id": 7},
    {"summary": "What is your favorite thing about our relationship?", "topic_str":"romantic", "topic":3, "id": 8},
    {"summary": "What is the most thoughtful gift you have ever received?", "topic_str":"romantic", "topic":3, "id": 16},
    {"summary": "What is your idea of a perfect kiss?", "topic_str":"romantic", "topic":3, "id": 17},
    {"summary": "What is your idea of a perfect date?", "topic_str":"romantic", "topic":3, "id": 18},

    # topic sexy
    {"summary": "What is your favorite thing about my body?", "topic_str":"sexy", "topic":0, "id": 9},
    {"summary": "What is your favorite thing about my personality?", "topic_str":"sexy", "topic":0, "id": 10},
    {"summary": "What would you do with my body if you had it for a day?", "topic_str":"sexy", "topic":0, "id": 11},
    {"summary": "What is the sexiest thing someone has ever done to you?", "topic_str":"sexy", "topic":0, "id": 19},
    {"summary": "What is the sexiest thing you have ever done?", "topic_str":"sexy", "topic":0, "id": 20},
    {"summary": "What is the sexiest quality you find in a partner?", "topic_str":"sexy", "topic":0, "id": 21},

    # topic interesting
    {"summary": "Have you ever heard about N vs NP problem?", "topic_str":"interesting", "topic":2, "id": 12},
    {"summary": "What is the most fascinating technology you have seen recently?", "topic_str":"interesting", "topic":2, "id": 22},
    {"summary": "What is the most interesting place you have ever visited?", "topic_str":"interesting", "topic":2, "id": 23},
    {"summary": "What is the most fascinating scientific discovery you have heard of?", "topic_str":"interesting", "topic":2, "id": 24},

    {"summary": "What is your favorite hobby?", "topic_str":"casual", "topic":1, "id": 25},
    {"summary": "What is the best trip you have ever been on?", "topic_str":"casual", "topic":1, "id": 26},
    {"summary": "What is your favorite type of cuisine?", "topic_str":"casual", "topic":1, "id": 27},

    {"summary": "What is the most romantic moment you have experienced?", "topic_str":"romantic", "topic":3, "id": 28},
    {"summary": "What is your idea of a perfect proposal?", "topic_str":"romantic", "topic":3, "id": 29},
    {"summary": "What is your idea of a perfect weekend getaway?", "topic_str":"romantic", "topic":3, "id": 30},

    {"summary": "What is the most intimate act you have ever experienced?", "topic_str":"sexy", "topic":0, "id": 31},
    {"summary": "What is the most intimate act you have ever performed?", "topic_str":"sexy", "topic":0, "id": 32},
    {"summary": "What is the most intimate place you have ever had sex?", "topic_str":"sexy", "topic":0, "id": 33},

    {"summary": "What is the most interesting book you have read recently?", "topic_str":"interesting", "topic":2, "id": 34},
    {"summary": "What is the most interesting talk you have ever attended?", "topic_str":"interesting", "topic":2, "id": 35},
    {"summary": "What is the most interesting thing you have learned this week?", "topic_str":"interesting", "topic":2, "id": 36},

    {"summary": "What is your favorite vacation destination?", "topic_str":"casual", "topic":1, "id": 37},
    {"summary": "What is your favorite type of music?", "topic_str":"casual", "topic":1, "id": 38},
    {"summary": "What is your favorite type of art?", "topic_str":"casual", "topic":1, "id": 39},

    {"summary": "What is the most romantic gift you have ever received?", "topic_str":"romantic", "topic":3, "id": 40},
    {"summary": "What is the most romantic thing you have ever done for someone?", "topic_str":"romantic", "topic":3, "id": 41},
    {"summary": "What is your ideal romantic getaway destination?", "topic_str":"romantic", "topic":3, "id": 42},

    {"summary": "What is your favorite aspect of a person's sexual appeal?", "topic_str":"sexy", "topic":0, "id": 43},
    {"summary": "What is the sexiest fantasy you have ever had?", "topic_str":"sexy", "topic":0, "id": 44},
    {"summary": "What is the hottest sexual encounter you have ever had?", "topic_str":"sexy", "topic":0, "id": 45},

    {"summary": "What is the most interesting scientific discovery you have heard about lately?", "topic_str":"interesting", "topic":2, "id": 46},
    {"summary": "What is the most interesting book you have read recently?", "topic_str":"interesting", "topic":2, "id": 47},
    {"summary": "What is the most interesting historical event you have learned about recently?", "topic_str":"interesting", "topic":2, "id": 48},
] + truth_topic + sexy_topic + casual_topic

topics_map = [
    {
        "id": 1,
        "topic_str": "Casual",
        "topic_icon": "cloudyNight"
    },
    {
        "id": 4,
        "topic_str": "Truth",
        "topic_icon": "checkmark"
    },
    {
        "id": 0,
        "topic_str": "Sexy",
        "topic_icon": "flame"
    },
    {
        "id": 2,
        "topic_str": "Interesting",
        "topic_icon": "bulb"
    },
    {
        "id": 3,
        "topic_str": "Romantic",
        "topic_icon": "heart"
    },
]
