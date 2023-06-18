#!/bin/bash 

sudo ip netns add ns1
sudo ip netns add ns2
echo "namespaces created"

sudo ip link add veth1 type veth peer name veth1-br
sudo ip link add veth2 type veth peer name veth2-br
echo "veths created"


sudo ip link set veth1 netns ns1
sudo ip link set veth2 netns ns2
echo "veths set"


sudo ip netns exec ns1 ip addr add 10.0.0.2/24 dev veth1
sudo ip netns exec ns2 ip addr add 10.0.0.3/24 dev veth2
echo "ip addresses set"

sudo ip link add name br0 type bridge
echo "bridge created"

sudo ip link set veth1-br master br0
sudo ip link set veth2-br master br0
echo "veths added to bridge"


sudo ip link set veth1-br up
sudo ip link set veth2-br up
sudo ip netns exec ns1 ip link set veth1 up
sudo ip netns exec ns2 ip link set veth2 up
echo "veths up"

sudo ip link set br0 up
echo "bridge up"

sudo ip addr add 10.0.0.1/24 dev br0
echo "bridge ip set"


sudo ip netns exec ns1 ip route add default via 10.0.0.1
sudo ip netns exec ns2 ip route add default via 10.0.0.1
echo "default routes set"


sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

sudo iptables -t nat -A POSTROUTING -o wlp3s0 -j MASQUERADE

sudo iptables -A FORWARD -i wlp3s0 -o br0 -m state --state RELATED,ESTABLISHED -j ACCEPT

sudo iptables -A FORWARD -i br0 -o wlp3s0 -j ACCEPT

# Allow DNS (this must be done for the server namespace because mongodb needs to resolve the hostname)
sudo ip netns exec ns1 echo "nameserver 8.8.8.8" > /etc/resolv.conf

# enable ip forwarding
iptables --policy FORWARD ACCEPT

# setup packetloss on the ns1
#sudo ip netns exec ns1 tc qdisc add dev veth1 root netem loss 20%