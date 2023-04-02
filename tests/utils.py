import subprocess
import os
import time
import pymongo
import pandas as pd
from datetime import datetime
from math import sqrt

def connect_to_mongo():
    
    # connect to mongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client

def stop_containers():
    subprocess.run(["docker-compose", "down"])  # Stop and remove containers

def get_loss_from_doc(doc):

    raw_data = doc["raw_data"]
    epoch = doc["meta_data"]["epoch"]
    time = datetime.fromtimestamp(epoch/1000)

    # create df from the last inserted document

    df = pd.DataFrame(raw_data)

    # the number of received packets
    received_packets = len(df[df["received"] == True])
    dropped_packets = len(df[df["received"] == False])

    # calculate the packet loss
    packet_loss = dropped_packets / (received_packets + dropped_packets) * 100

    return packet_loss

def calculate_packetloss_bounds(expected_packet_loss, duration, frequency):

    # calculate the number of packets sent
    packets_sent = duration * frequency
    expected_packet_loss_decimal = expected_packet_loss / 100

    mean = expected_packet_loss_decimal
    std = sqrt(expected_packet_loss_decimal * (1 - expected_packet_loss_decimal) / packets_sent)

    # calculate the 99 % bounds
    lower_bound = mean - 2.58 * std
    upper_bound = mean + 2.58 * std

    return  lower_bound * 100, upper_bound * 100