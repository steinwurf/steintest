sudo ip link delete br0 type bridge
sudo ip -all netns delete
sudo ip link delete veth1-br
