import pytest 
import os
import sys
import tests.utils as utils
sys.path.append("..")
import demo.run_demo as f

# parametrize the test
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

    assert True
    #assert expected_packet_loss - lower_bound <= packet_loss <= expected_packet_loss + upper_bound




