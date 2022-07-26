import pymongo
import plotly.express as px



myclient = pymongo.MongoClient("mongodb+srv://PythonClient:4D0m68QC172aXo9T@db-mongo-81099e05.mongo.ondigitalocean.com/steintest?tls=true&authSource=admin&replicaSet=db-mongo")

db = myclient["steintest"]
collection = db["sessiondata"]

""" query = {"destinationserver" : "New York"}

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
    fig.show() """



document = collection.aggregate(
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

for doc in document:
    data = doc['res']

    fig = px.histogram(data )
    fig.show()
    