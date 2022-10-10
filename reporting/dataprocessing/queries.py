from pymongo import MongoClient
import pandas as pd
import geopy.distance




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
        return doc_list[0]['count']
    else:
        return 0

def get_num_tests_per_server(LAST_REPORT_DATE, servers):
    result_dict = {}
    for server in servers:
        result_dict[f"num_of_tests_{server.lower().replace(' ', '_')}"] = 0



    query_result = client['steintest']['sessiondata'].aggregate([
    {
        '$match': {
            'TimeStamp': {
                '$gt': LAST_REPORT_DATE
            }, 
            'destinationserver': {
                '$ne': None
            }
        }
    }, {
        '$sortByCount': '$destinationserver'
        }
    ])
    
    for doc in query_result:
        doc_name = f"num_of_tests_{doc['_id'].lower().replace(' ', '_')}"
        if doc_name in result_dict:
            result_dict[doc_name] = doc['count']
    
    return result_dict


def get_num_tests_per_continent(LAST_REPORT_DATE, continents):
    result_dict = {}

    for continent in continents:
        result_dict[f"num_of_tests_{continent.lower().replace(' ', '_')}"] = 0

    query_result = client['steintest']['sessiondata'].aggregate([
    {
        '$match': {
            'TimeStamp': {
                '$gt': LAST_REPORT_DATE
            }, 
            'GeoLocation.continentName': {
                '$ne': None
            }
        }
    }, {
        '$sortByCount': '$GeoLocation.continentName'
    }
    ])

    for doc in query_result:
        doc_name = f"num_of_tests_{doc['_id'].lower().replace(' ', '_')}"
        if doc_name in result_dict:
            result_dict[doc_name] = doc['count']

    return result_dict

def get_array_of_cons_lost_packets(LAST_REPORT_DATE):
    query_result = client['steintest']['sessiondata'].aggregate([
        {
            '$match': {
                'ConsLostPacketData': {
                    '$ne': None
                }, 
                'TimeStamp': {
                    '$gt': 0
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
    ])
    result = list(query_result)
    if len(result) == 1:
        return result[0]['res']


def get_timestamp_for_all_tests ():
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
        '$group': {
            '_id': 'TimeStamp', 
            'res': {
                '$push': '$TimeStamp'
            }
        }
    }
    ])

    result = list(query_result)
    if len(result) == 1:
        return result[0]['res']


def get_tests_over_time_per_server():
    query_result = client['steintest']['sessiondata'].aggregate([
    {
        '$match': {
            'TimeStamp': {
                '$ne': None
            }, 
            'destinationserver': {
                '$ne': None
            }
        }
    }, {
        '$group': {
            '_id': '$destinationserver', 
            'res': {
                '$push': '$TimeStamp'
            }
        }
    }
    ])
    return list(query_result)


def get_tests_over_time_per_continent():
    query_result = client['steintest']['sessiondata'].aggregate([
    {
        '$match': {
            'TimeStamp': {
                '$ne': None
            }, 
            'GeoLocation.continentName': {
                '$ne': None
            }
        }
    }, {
        '$group': {
            '_id': '$GeoLocation.continentName', 
            'res': {
                '$push': '$TimeStamp'
            }
        }
    }
    ])
    return list(query_result)


def get_distance_to_server_for_each_test():

    query_result = client['steintest']['sessiondata'].aggregate([
        {
            '$match': {
                'destinationserver': {
                    '$ne': None
                }, 
                'GeoLocation.latitude': {
                    '$ne': None
                }, 
                'GeoLocation.longitude': {
                    '$ne': None
                }
            }
        }, {
            '$project': {
                'destinationserver': 1, 
                'ClientLatitude': '$GeoLocation.latitude', 
                'ClientLongitude': '$GeoLocation.longitude', 
                '_id': 0, 
                'PacketLossPercentage': 1
            }
        }, {
            '$lookup': {
                'from': 'servers', 
                'localField': 'destinationserver', 
                'foreignField': 'ServerName', 
                'as': 'result'
            }
        }, {
            '$unwind': {
                'path': '$result', 
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$project': {
                'destinationserver': 1, 
                'ClientLatitude': 1, 
                'ClientLongitude': 1, 
                'ServerLatitude': '$result.Location.latitude', 
                'ServerLongitude': '$result.Location.longitude', 
                '_id': 0, 
                'PacketLossPercentage': 1
            }
        }
    ])

    result = list(query_result)
    df = pd.DataFrame.from_records(result)
    df['distance'] = df.apply(lambda row: geopy.distance.geodesic((row['ClientLatitude'], row['ClientLongitude']), (row['ServerLatitude'], row['ServerLongitude'])).km, axis=1)
    return df


def get_packetloss_per_OS():
    query_result = client['steintest']['sessiondata'].aggregate([
    {
        '$match': {
            'PacketLossPercentage': {
                '$ne': None
            }, 
            'UserAgent.OS': {
                '$ne': None
            }
        }
    }, {
        '$project': {
            'PacketLossPercentage': 1, 
            'OS': '$UserAgent.OS', 
            '_id': 0
        }
    }
    ])

    result =  list(query_result)

    df = pd.DataFrame.from_records(result)
    return df


def get_packetloss_and_speed():
    query_result = client['steintest']['sessiondata'].aggregate([
    {
        '$match': {
            'PacketLossPercentage': {
                '$ne': None
            }, 
            'Frequency': {
                '$ne': None
            }, 
            'PacketSize': {
                '$ne': None
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'PacketLossPercentage': 1, 
            'Speed': {
                '$multiply': [
                    '$Frequency', '$PacketSize'
                ]
            }
        }
    }
    ])

    result =  list(query_result)
    df = pd.DataFrame.from_records(result)

    df['Speed'] = df['Speed'].apply(lambda x: (x * 8) / 1000000)

    return df


def get_latency_and_packetloss_for_each_test():
    query_result = client['steintest']['sessiondata'].aggregate([
    {
        '$match': {
            'PacketLossPercentage': {
                '$ne': None
            }, 
            'TestData': {
                '$ne': None
            }
        }
    }, {
        '$unwind': {
            'path': '$TestData', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$group': {
            '_id': '$_id', 
            'Latency': {
                '$avg': '$TestData.delay'
            }, 
            'PacketLossPercentage': {
                '$first': '$PacketLossPercentage'
            }
        }
    }, {
        '$project': {
            'Latency': 1, 
            'PacketLossPercentage': 1, 
            '_id': 0
        }
    }
    ])

    result =  list(query_result)
    df = pd.DataFrame.from_records(result)

    return df
    
def get_tests_packetloss_and_continent():
    query_result = client['steintest']['sessiondata'].aggregate([
    {
        '$match': {
            'PacketLossPercentage': {
                '$ne': None
            }, 
            'GeoLocation.continentName': {
                '$ne': None
            }
        }
    }, {
        '$project': {
            'PacketLossPercentage': 1, 
            '_id': 0, 
            'Continent': '$GeoLocation.continentName'
        }
    }
    ])

    result =  list(query_result)
    df = pd.DataFrame.from_records(result)
    return df 

def get_number_of_lost_packets_per_test():
    query_result = client['steintest']['sessiondata'].aggregate(
        [
        {
            '$match': {
                'TimeStamp': {
                    '$gt': 0
                }, 
                'NumberOfPackets': {
                    '$ne': None
                }, 
                'PacketLossPercentage': {
                    '$ne': None
                }, 
                'IP': {
                    '$ne': None
                }
            }
        }, {
            '$project': {
                'number_of_lost_packets': {
                    '$round': {
                        '$multiply': [
                            '$NumberOfPackets', '$PacketLossPercentage', 0.01
                        ]
                    }
                },
                '_id': 0,
            }
            
        }
        ]
    )

    df = pd.DataFrame.from_records(list(query_result))
    return df
