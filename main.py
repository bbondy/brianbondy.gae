# Standard Python imports.
#import os
#import sys
#import logging

import sys
sys.path.insert(0, 'libs')
sys.path.insert(0, 'libs/reportlab.zip')

#import webapp2;
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from app import *
from urls import *


#@application.route("/")
#def hello():
#    return "Hello World!"

#@application.route("/jsontest")
#def jsontest():
#  return jsonify(**{'test1': 'hello1', 'test3': 3, 'test3': [1,2,3], 'x': (1,2,3)})

#@application.route('/users/', defaults={'name': 'brian'})
#@application.route("/about/<name>/")
#def about(name):
#    return "About" + name + "!"


#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        do_the_login()
#    else:
#        show_the_login_form()


#@application.route('/hello/')
#@application.route('/hello/<name>')
#def hello2(name=None):
#    return render_template('about.html', name=name)

# Create a Django application for WSGI.
#application = webapp2.WSGIApplication(urls.routes, debug=True);


#For safe markup
#from flask import Markup
#>>> Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'


#URL Params
#searchword = request.args.get('key', '')


#Redirect and errors
#@app.route('/')
#def index():
#    return redirect(url_for('login'))
#@app.route('/login')
#def login():
#    abort(401)
#    this_is_never_executed()


#int, float, string, path
#@app.route('/post/<int:post_id>')
#def show_post(post_id):
#    pass
