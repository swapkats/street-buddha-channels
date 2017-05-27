#!flask/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from nsetools import Nse

import simplejson as json

nse = Nse()
app = Flask(__name__)
CORS(app)

def get_quote_details(quote_code):
    codes = nse.get_quote(str(quote_code), as_json=True)
    codes = json.loads(codes)
    res = {
        'closePrice': codes['closePrice'],
        'change': codes['change'],
        'companyName': codes['companyName'],
        'dayHigh': codes['dayHigh'],
        'dayLow': codes['dayLow'],
        'symbol': codes['symbol'],
        'totalTradedVolume': codes['totalTradedVolume'],
        'previousClose': codes['previousClose'],
        'open': codes['open'],
        'low52': codes['low52'],
        'high52': codes['high52'],
        'exDate': codes['exDate'],
        'low52': codes['low52'],
        'low52': codes['low52'],
    }
    return codes

@app.route('/api/v1.0/quotes/<string:quote_code>', methods=['GET'])

def get_quote(quote_code):
    res = get_quote_details(quote_code)
    return jsonify(res)

@app.route('/api/v1.0/quotes', methods=['POST'], endpoint='get_quotes')

def get_quotes():
    quotes = {}
    payload = request.get_json()
    positions = payload['positions']
    for position in positions:
        quotes[position['s']] = get_quote_details(position['s'])
    return jsonify(quotes)
