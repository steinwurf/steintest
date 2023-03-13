from pathlib import Path
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from math import sqrt
import time
import logging


demo_path = Path(__file__).resolve().parents[1] / "demo"
connection_string_path = demo_path / "connection_string.txt"
def load_connection_string():
    with open(connection_string_path, 'r') as f:
        return f.read()

def get_loss_from_last_test():

    client = MongoClient(host="localhost", port=27017)
    db = client['test']
    col = db["test"]

    # retrieve the last inserted document
    last_doc = col.find().sort([('_id', -1)]).limit(1)[0]

    raw_data = last_doc["raw_data"]
    epoch = last_doc["meta_data"]["epoch"]
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


if __name__ == "__main__":
    print(load_connection_string())