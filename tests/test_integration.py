import pytest 
import os
import sys
import tests.utils as utils
sys.path.append("..")
import demo.run_demo as f
import subprocess
import time

""" # parametrize the test
@pytest.mark.parametrize("expected_packet_loss", [2])
@pytest.mark.parametrize("duration", [5])
@pytest.mark.parametrize("frequency", [100])
@pytest.mark.parametrize("packet_size", [100])
def test_integration(expected_packet_loss, duration, frequency, packet_size):
    os.chdir(str(utils.demo_path))

    f.run_full_demo(expected_packet_loss, duration, frequency, packet_size)

    # get the test result

    packet_loss = utils.get_loss_from_last_test()

    # calculate the bounds
    lower_bound, upper_bound = utils.calculate_packetloss_bounds(expected_packet_loss, duration, frequency)

    assert expected_packet_loss - lower_bound <= packet_loss <= expected_packet_loss + upper_bound """

@pytest.mark.parametrize("expected_packet_loss", [2])
@pytest.mark.parametrize("duration", [5])
@pytest.mark.parametrize("frequency", [100])
@pytest.mark.parametrize("packet_size", [100])
def test1_integration(expected_packet_loss, duration, frequency, packet_size):
    os.chdir(str(utils.demo_path))

    # run the server 
    server = subprocess.Popen(["sudo ip netns exec ns1 ./server", "-serverParams server_params.json"], shell=True)

    # run the client
    client = subprocess.Popen(["sudo ip netns exec ns2 ./client", "-clientParams"], shell=True)

    # wait 1 minute
    time.sleep(60)

    # kill the server
    server.kill()

    # kill the client
    client.kill()

    # get the test result

    packet_loss = utils.get_loss_from_last_test()

    # calculate the bounds
    lower_bound, upper_bound = utils.calculate_packetloss_bounds(expected_packet_loss, duration, frequency)

    assert expected_packet_loss - lower_bound <= packet_loss <= expected_packet_loss + upper_bound


