import mysql.connector
import flask
import sqlgetter #code i made to return a connection to my database i have been using it for my homework

from flask import jsonify
from flask import request

app = flask.Flask(__name__)
app.config['DEBUG'] = True
con = sqlgetter.createConnection()