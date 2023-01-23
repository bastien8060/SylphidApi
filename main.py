#!/bin/python3
# SylphidAPI: Python3 Api server for Android CapacitorJS App 
# (c) 2022 Sylphid

# It is aimed at couples and can suggest conversations, dates, test each other's love 
# language, save memories, games.
# Includes games such as DnD, convo opener, truth or dare, and more (using gpt3 API)
# It can also suggest movies, tv shows, and books to watch/read

from app import app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
