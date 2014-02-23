# check.py

import sys
import json
import argparse
import requests 
from datetime import datetime
from dateutil import parser
from flask import (
    Flask, render_template, request, jsonify,
)
from unipath import Path

TEMPLATE_DIR = Path(__file__).ancestor(1).child("templates")
URL = "http://www.bbc.co.uk/programmes/{programme}/episodes/player.json"
app = Flask(__name__, template_folder=TEMPLATE_DIR)


@app.route('/')
def index():
    """
    Return the main view.
    """
    return render_template('index.html')


@app.route('/api/', methods=['GET'])
def api():
    programme = request.args.get('programme', '', type=str)
    response = requests.get(URL.format(programme=programme))
    if response.status_code == requests.codes.ok:
        js = response.json()
        today = datetime.now()
        broadcast = parser.parse(
            js['episodes'][0]['programme']['first_broadcast_date']
        )
        check = today.strftime("%U") == broadcast.strftime("%U") 
        last_episode_number = js['episodes'][0]['programme']['position']
        success = True
    else:
        check = False
        success = False
    return jsonify(
        {
            "success": success,
            "check": check,
            "programme": programme,
            "last_episode_number": last_episode_number,
        }
    )


def main():
    """
    Main entry point for script.
    """
    app.run(debug=True)


if __name__ == '__main__':
    sys.exit(main())