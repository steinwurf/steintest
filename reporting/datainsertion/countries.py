
from pymongo import MongoClient
import pandas as pd

# This file is used to insert the data into the database for the countries location and name
# This file is not meant to be run unless you want to update the data in the database
# And in that case you should run this file after the data has been updated in the csv file


df = pd.read_csv("data/countries.csv")

client = MongoClient('mongodb+srv://MongoCompass:t2GE6041Di9H7g5C@db-mongo-81099e05.mongo.ondigitalocean.com/steintest?tls=true&authSource=admin&replicaSet=db-mongo')

db = client['steintest']

collection = db['countries']

records = df.to_dict(orient='records')

collection.insert_many(records)

# This is the end of the file
