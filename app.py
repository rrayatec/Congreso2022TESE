from flask import Flask, redirect, url_for, request, render_template, make_response, session, jsonify
from werkzeug.exceptions import MethodNotAllowed
from pymongo import MongoClient, cursor
#from twilio.rest import Client
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

@app.route("/")
def home():
    cursor = cuentas.find({})
    user = []
    for doc in cursor:
        user.append(doc)

    return render_template("/Retrieve.html", data=user)