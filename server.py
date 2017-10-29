#!/usr/bin/env python2
import json
import os
import requests

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, g, make_response
from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
auth = HTTPBasicAuth()

# Connect to Database and create database session
engine = create_engine('sqlite:///catelog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
if __name__ == '__main__':
    app.secret_key = '\x1a\xbeZ\xb7g\x1f\x00\xfe\x1a|s\x13y\xd8r)(E\x88\xa4go(\xc1'
    app.debug = True
    app.run(host='localhost', port=8000)
