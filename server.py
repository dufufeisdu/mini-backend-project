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
def show_category():
    items = session.query(Item).all()
    items = map(lambda x: [x.name, x.address,
                           x.category], items)

    return render_template('entry.html', items=items, is_logged_in=is_login())


@app.route('/<itemname>/details')
def show_detail(itemname):
    items = session.query(Item).all()
    item_names = list(map(lambda x: x.name, items))
    if itemname in item_names:
        item_descriptions = list(map(lambda x: x.description, items))
        description = item_descriptions[item_names.index(itemname)]
        return render_template('itemDetail.html', description=description)


@app.route('/login', methods=['GET', 'POST'])
def show_login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        admins = session.query(User).filter_by(title='Admin').all()
        all_admin_name = list(map(lambda x: x.username, admins))

        if username in all_admin_name:
            user = session.query(User).\
                filter_by(title='Admin').\
                filter_by(username=username).\
                one()
            if user.verify_password(password):
                login_session['username'] = username
                return redirect('/')

        response = make_response(json.dumps(
            'Invalid username or password.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def show_logout():
    del login_session['username']
    return redirect('/')


@app.route('/<itemname>/edit', methods=['GET', 'POST'])
def show_edit(itemname):
    if is_login():
        if request.method == 'GET':
            item = session.query(Item).filter_by(name=itemname).one()
            return render_template('edit.html', name=item.name,
                                   description=item.description, category=item.category, address=item.address)
        if request.method == 'POST':
            item = session.query(Item).filter_by(name=itemname).one()
            item.name = request.form.get('name', None)
            item.address = request.form.get('address', None)
            item.category = request.form.get('category', None)
            item.description = request.form.get('description', None)
            session.add(item)
            session.commit()
            return redirect('/')
    response = make_response(json.dumps(
        'You must login first'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/<itemname>/delete')
def delete(itemname):

    return redirect('/')


if __name__ == '__main__':
    app.secret_key = '\x1a\xbeZ\xb7g\x1f\x00\xfe\x1a|s\x13y\xd8r)(E\x88\xa4go(\xc1'
    app.debug = True
    app.run(host='localhost', port=5050)
