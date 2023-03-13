
import dummynet
import logging
import time
import subprocess
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

def run_full_demo(packetloss, duration, frequency, packet_size):
    # runs the full demo with the given parameters

    try:
        # setup the namespaces and bridge
        process_monitor, net, shell, ns1, ns2 = setup_namespaces()

        # add packetloss to veth1
        #ns1.run(cmd=f"tc qdisc add dev veth1 root netem loss {packetloss}%")
        add_packetloss(ns1, "veth1", packetloss)

        # Run the server and client in the namespaces
        server = run_server(ns1)
        time.sleep(2)

        client = run_client(ns2, duration, frequency, packet_size)

        while process_monitor.run():
            pass
            
    except Exception as e:
        print(e)
        
    finally:        
        cleanup(net, shell)

def setup_namespaces():
    # sets the namespaces and bridge up
    log = logging.getLogger("dummynet")
    log.setLevel(logging.DEBUG)

    process_monitor = dummynet.ProcessMonitor(log=log)

    shell = dummynet.HostShell(log=log, sudo=True, process_monitor=process_monitor)

    net = dummynet.DummyNet(shell=shell)

    try:
        # Get a list of the current namespaces
        namespaces = net.netns_list()
        assert namespaces == []

        # create two namespaces
        ns1 = net.netns_add(name="ns1")
        ns2 = net.netns_add(name="ns2")

        net.link_veth_add(p1_name="veth1", p2_name="veth1-br")
        net.link_veth_add(p1_name="veth2", p2_name="veth2-br")


        # Move the interfaces to the namespaces
        net.link_set(namespace="ns1", interface="veth1")
        net.link_set(namespace="ns2", interface="veth2")

        # Bind an IP-address to the two peers in the link.
        ns1.addr_add(ip="10.0.0.2/24", interface="veth1")
        ns2.addr_add(ip="10.0.0.3/24", interface="veth2")

        # Create a bridge
        net.bridge_add(name="br0")


        # Add the two peers to the bridge
        net.bridge_set(interface="veth1-br", name="br0")
        net.bridge_set(interface="veth2-br", name="br0")


        # Bring up the interfaces
        net.up(interface="veth1-br")
        net.up(interface="veth2-br")
        ns1.up(interface="veth1")
        ns2.up(interface="veth2")

        # Bring up the bridge
        net.bridge_up(name="br0")

        # assign IP to bridge
        net.addr_add(ip="10.0.0.1/24", interface="br0")

        # add default route
        ns1.route("10.0.0.1")
        ns2.route("10.0.0.1")

        shell.run(cmd='sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"')
        shell.run(cmd='sudo iptables -t nat -A POSTROUTING -o wlp3s0 -j MASQUERADE')
        shell.run(cmd='sudo iptables -A FORWARD -i wlp3s0 -o br0 -m state --state RELATED,ESTABLISHED -j ACCEPT')
        shell.run(cmd='sudo iptables -A FORWARD -i br0 -o wlp3s0 -j ACCEPT')
        # enable ip forwarding
        shell.run(cmd='iptables --policy FORWARD ACCEPT')

        return process_monitor, net, shell, ns1, ns2
    except Exception as e:
        print(e)
        #cleanup(net, shell)
        raise e

def add_packetloss(ns, interface, packetloss=0, delay=0):
    # add packetloss to the given namespace
    ns.tc(interface=interface, loss=packetloss, delay=delay)

def run_client(ns, duration, frequency, packet_size):
    # run the client in the second namespace
    def _client_stdout(data):
        print("client {}".format(data))
        pass
        
    client = ns.run_async(cmd=f"./client -Ip 10.0.0.2 -Duration {duration} -Frequency {frequency} -PacketSize {packet_size}", daemon=False)

    client.stdout_callback = _client_stdout

    return client

def run_server(ns):
    # run the server in the first namespace
    server = ns.run_async(cmd="./server -serverParams serverParams.json", daemon=False)

    def _server_stdout(data):
        print("server {}".format(data))
        if "inserted data" in data:
            # the server has inserted data into the database
            # and we can stop the client and server
            raise Exception("demo is finished")

    server.stdout_callback = _server_stdout

    return server

def cleanup(net, shell):
    # delete the namespaces and bridge

    # Clean up.
    net.cleanup()
    print("deleting veths")
    try:
        shell.run('sudo ip link delete veth1-br type veth')
    except:
        pass
    try:
        shell.run('sudo ip link delete veth2-br type veth')
    except:
        pass
    try:
        shell.run('sudo ip link delete br0 type bridge')
    except:
        pass
        

def print_test_result():
    client = MongoClient(load_connection_string())
    db = client['test']
    col = db["default"]

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

    print("packet loss: {}%".format(round(packet_loss, 2)))
    print("received packets: {}".format(received_packets))
    print("dropped packets: {}".format(dropped_packets))
    print("time: {}".format(time))


def load_connection_string():
    with open('connection_string.txt', 'r') as f:
        return f.read()
        

def run_mock_test_shell(packetloss, duration=10, frequency=150, packet_size=1024):
    
    # run the demo in a shell and just kill both subprocess when an extensive amount of time has passed

    try:
        # create the namespaces 
        subprocess.run(["sudo","sh", "sh_demo/create_ns.sh"])

        # add packetloss to veth1
        subprocess.run(["sudo", "ip", "netns", "exec", "ns1", "tc", "qdisc", "add", "dev", "veth1", "root", "netem", "loss", "{}%".format(float(packetloss))])

        # run the server and client in the namespaces
        server_process = subprocess.Popen(["sudo", "ip", "netns", "exec", "ns1","./server", "-serverParams", "serverParams.json"])

        client_process = subprocess.Popen(["sudo", "ip", "netns", "exec", "ns2","./client", "-Ip", "10.0.0.2"])

        print("sleeping for {} seconds".format(duration*2))
        time.sleep(duration * 2)
        print("slept for {} seconds".format(duration*2))


        
    except Exception as e:
        print(e)
    finally:

        subprocess.run(["sudo","sh", "sh_demo/cleanup.sh"])

if __name__ == "__main__":
    #process_monitor, net, shell, ns1, ns2 = setup_namespaces()
    for i in [1,10, 30]:
        run_full_demo(packetloss=i, duration=10, frequency=150, packet_size=1024)
        print_test_result()
    print("Demo finished")

    #cleanup(net, shell)

