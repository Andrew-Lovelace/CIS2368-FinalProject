import mysql.connector
import flask
import sqlgetter #code i made to return a connection to my database i have been using it for my homework
import hashlib

from flask import jsonify
from flask import request

app = flask.Flask(__name__)
app.config['DEBUG'] = True
con = sqlgetter.createConnection()

@app.route("/api/<table>", methods=["GET"]) #the <> allows for this code be reused for all 3 table i learned about it from reading the online documentation https://www.geeksforgeeks.org/flask-app-routing/
def tableview(table):
    return sqlgetter.querry(con, table)

@app.route("/api/<table>", methods=["POST"])
def booksadd(table):
    userinput = request.get_json()
    sqlgetter.insert(con,table, userinput)

@app.route("/api/customer", methods=["POST"]) #i use customers without an s when the table hasone to allow the funtion with <> to still work incase the encoding happens on the front end for some reason
def customersadd():
    userinput = request.get_json()
    userinput['passwordhash'] = hashlib.sha256(userinput['passwordhash'].encode()).hexdigest()
    sqlgetter.insert(con, 'customers', userinput)

@app.route("/api/<table>", methods=["PUT"])
def tableupdate(table):
    userinput = request.get_json()
    where = sqlgetter.dictodouble(userinput,["id"])
    sqlgetter.update(con, table,where[0], where[1])

@app.route("/api/<table>",methods=["DELETE"])
def tabledelete(table):
    userinput = request.get_json()
    where = sqlgetter.dicttosignle(userinput)
    sqlgetter.remove(con,table,where)


#app.run()
sqlgetter.insert(con, "borrowingrecords","yes")