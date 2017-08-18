#!/usr/bin/env python

from flask import Flask
import re
app = Flask(__name__)

@app.route('/')

@app.route('/', methods=['GET','POST'])
def test():

	if request.method == "POST":
		clicked=request.json['data']
		return clicked