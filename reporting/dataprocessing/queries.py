from pymongo import MongoClient

client = MongoClient('mongodb+srv://MongoCompass:t2GE6041Di9H7g5C@db-mongo-81099e05.mongo.ondigitalocean.com/steintest?tls=true&authSource=admin&replicaSet=db-mongo')

def get_num_tests_since_last_report(LAST_REPORT_DATE):
    query_result = client['steintest']['sessiondata'].aggregate([
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
        '$match': {
            'TimeStamp': {
                '$gt': LAST_REPORT_DATE
            }
        }
    }, {
        '$count': 'count'
    }
    ])
    doc_list = list(query_result)

    if len(doc_list) == 1:
        print(doc_list[0]['count'])
        return doc_list[0]['count']
    else:
        print(-1)
        return -1

#print(get_num_tests_since_last_report())
