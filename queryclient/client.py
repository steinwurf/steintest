import pymongo
import plotly.express as px
import pandas as pd


myclient = pymongo.MongoClient("mongodb+srv://PythonClient:4D0m68QC172aXo9T@db-mongo-81099e05.mongo.ondigitalocean.com/steintest?tls=true&authSource=admin&replicaSet=db-mongo")

db = myclient["steintest"]
collection = db["sessiondata"]

document = collection.aggregate([
    {
        '$unwind': {
            'path': '$TestData'
        }
    }, {
        '$project': {
            'TestData.delay': 1
        }
    }, {
        '$group': {
            '_id': '_id', 
            'res': {
                '$push': '$TestData.delay'
            }
        }
    }, {
        '$project': {
            'res': 1, 
            '_id': 0
        }
    }
])


for doc in document:
    data = doc['res']

    fig = px.ecdf(data, ecdfmode="reversed" )
    fig.show()


""" 
documents = collection.aggregate(
    [
    {
        '$match': {
            'ConsLostPacketData': {
                '$ne': None
            }
        }
    }, {
        '$project': {
            'ConsLostPacketData': 1, 
            '_id': 0
        }
    }, {
        '$unwind': {
            'path': '$ConsLostPacketData'
        }
    }, {
        '$group': {
            '_id': 'Consecutive lost packets', 
            'res': {
                '$push': '$ConsLostPacketData'
            }
        }
    }
    ]
)

for doc in documents:
    data = doc['res']

    fig = px.histogram(data)
    fig.show()

 """


""" documents = collection.aggregate(
    [
    {
        '$match': {
            'PacketLossPercentage': {
                '$ne': None
            }, 
            'IP': {
                '$ne': '['
            }, 
            'PacketSize': {
                '$ne': None
            }
        }
    }, {
        '$project': {
            'PacketLossPercentage': 1, 
            '_id': 0, 
            'PacketSize': 1
        }
    }
]
)

AllDocuments = {}

for index, doc in enumerate(documents):
    AllDocuments[index] = doc

df = pd.DataFrame(AllDocuments)
df = df.transpose()

fig = px.scatter(x=df['PacketSize'], y=df['PacketLossPercentage'])

fig.show() """