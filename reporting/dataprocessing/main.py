from pymongo import MongoClient
from matplotlib.dates import date2num, num2date
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import plotly.express as px
from datetime import datetime


# Requires the PyMongo package.

# https://api.mongodb.com/python/current

client = MongoClient('mongodb+srv://MongoCompass:t2GE6041Di9H7g5C@db-mongo-81099e05.mongo.ondigitalocean.com/steintest?tls=true&authSource=admin&replicaSet=db-mongo')
result = client['steintest']['sessiondata'].aggregate([
    {
        '$match': {
            'TimeStamp': {
                '$ne': None
            }
        }
    }, {
        '$project': {
            'TimeStamp': 1, 
            '_id': 0
        }
    }, {
        '$group': {
            '_id': 'TimeStamp', 
            'res': {
                '$push': '$TimeStamp'
            }
        }
    }
])

for doc in result:
    datetimes = doc["res"]




def createPlots(num_dates):
    datetimes = [datetime.utcfromtimestamp(num / 1000).strftime('%m-%d-%Y') for num in num_dates]

    fig = px.ecdf(datetimes, ecdfnorm=None)
    fig.show()

createPlots(datetimes)

