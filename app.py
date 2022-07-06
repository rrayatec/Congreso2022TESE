from flask import Flask, redirect, url_for, request, render_template, make_response, session, json, jsonify
from werkzeug.exceptions import MethodNotAllowed
from pymongo import MongoClient, cursor
# from twilio.rest import Client
import pymongo
import datetime
from decouple import config

config.encoding = 'cp1251'

# FlASK
#############################################################
app = Flask(__name__)
app.secret_key = "super secret key"
#############################################################

# MONGODB
#############################################################
mongodb_key = config('mongodb_key')
client = pymongo.MongoClient(mongodb_key)
db = client.test
cuentas = db.reports
#############################################################

# Twilio
##############################################################
# account_sid = config('account_sid')
# auth_token = config('auth_token')
# TwilioClient = Client(account_sid, auth_token)

#############################################################


@app.route("/", methods=['GET'])
def home():

    try:
        cursor = cuentas.find({})
        user = []
        for doc in cursor:
            user.append(doc)

        return render_template("/users.html", data=user)
    except Exception as e:
        return jsonify({"response": e})


@app.route("/graph", methods=['GET'])
def graph():
    try:
        data = json.dumps([0, 10, 5, 2, 20, 30, 45])
        labels = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
        ]

        return render_template("/graph.html", data=data, labels=labels)
    except Exception as e:
        return jsonify({"response": e})


@ app.route('/insert', methods=["POST"])
def insert():

    intent = {
        "intent": request.form['intent']
    }
    try:
        cuentas.insert_one(intent)
        return jsonify({"response": "ok"})

    except Exception as e:
        return jsonify({"response": e})
