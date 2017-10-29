#!/usr/bin/env python2
import json
import os
import requests
from init_database import Base, User, Item
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, g, make_response
from flask import session as login_session
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
auth = HTTPBasicAuth()

# Connect to Database and create database session
engine = create_engine('sqlite:///catelog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def is_login():
    if 'username' in login_session:
        return True
    else:
        return False


@app.route('/')
def showCategory():
    items = session.query(Item).all()
    description = map(lambda x: x.description, items)
    items = map(lambda x: [x.name, x.address,
                           x.category], items)

    return render_template('entry.html', items=items, description=description, is_logged_in=is_login())


@app.route('/')
def show_login():
    return render_template('login.html')


@app.route('/')
def show_logout():
    del login_session['username']
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = '\x1a\xbeZ\xb7g\x1f\x00\xfe\x1a|s\x13y\xd8r)(E\x88\xa4go(\xc1'
    app.debug = True
    app.run(host='localhost', port=5050)
