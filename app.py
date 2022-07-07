from flask import Flask, redirect, url_for, request, render_template, make_response, session, json, jsonify
from werkzeug.exceptions import MethodNotAllowed
from pymongo import MongoClient, cursor
# from twilio.rest import Client
from collections import Counter
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
        intents = []
        resultantList = []
        for doc in cursor:
            intents.append(doc["intent"])

        for element in intents:
            if element not in resultantList:
                resultantList.append(element)

        return render_template("/users.html", data=resultantList)
    except Exception as e:
        return jsonify({"response": e})


@app.route("/graph", methods=['GET'])
def graph():

    try:
        data = []
        resultantList = []

        cursor = cuentas.find({})
        intents = []
        for doc in cursor:
            intents.append(doc["intent"])

        for element in intents:
            if element not in resultantList:
                resultantList.append(element)
                data.append(intents.count(element))

        return render_template("/graph.html", data=data, labels=resultantList)
    except Exception as e:
        return jsonify({"response": e})


@ app.route('/insert', methods=["POST"])
def insert():

    try:
        cuentas.insert_one({
            "intent": request.json["intent"]
        })
        return jsonify({"response": "ok"})

    except Exception as e:
        return jsonify({"response": e})
