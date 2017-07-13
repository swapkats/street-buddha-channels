#!flask/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from nsetools import Nse
import logging

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
    return res

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

@app.route('/api/v1.0/symbols', methods=['GET'], endpoint='get_symbols')

def get_symbols():
  all_stock_symbols = nse.get_stock_codes()
  #symbols = json.loads(all_stock_symbols)
  # symbols = {}
  # for symbol in all_stock_symbols:
  #   symbols[symbol] = all_stock_symbols[symbol].encode('UTF-8', 'replace')
  # return jsonify(all_stock_symbols)
  return json.dumps(all_stock_symbols, encoding='latin1') # jsonify(symbols)
