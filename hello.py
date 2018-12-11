# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 11:07:33 2018

@author: YEOHANBOON
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'