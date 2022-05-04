#!/usr/bin/python3
from flask import Flask, jsonify
import helpers as h

app = Flask(__name__)

@app.route('/')
def index():
  return 'GTON API Operational'
  
@app.route('/circulating_supply')
def circulating_supply():
  return jsonify(h.get_csupply())

@app.route('/floor_price')
def floor_price():
  return jsonify(h.get_floor_price())


if __name__ == '__main__':
    app.run(debug=False)