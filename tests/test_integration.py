import pytest
import pymongo
import socket
import time
import subprocess
import os
import utils
import docker


@pytest.mark.parametrize("duration", [1])
@pytest.mark.parametrize("packet_size", [100])
@pytest.mark.parametrize("packet_loss", [0, 5, 10, 20])
@pytest.mark.parametrize("packet_delay", [0])
@pytest.mark.parametrize("frequency", [100])
def test_integration(duration, packet_size, packet_loss, packet_delay, frequency):
    try:
        env_vars = {
            "DURATION": str(duration),
            "PACKETSIZE": str(packet_size),
            "LOSS_RATE": str(packet_loss),
            "PACKET_DELAY": str(packet_delay),
            "FREQUENCY": str(frequency),
        }

        docker_compose_cmd = ["docker-compose", "up"]
        for key, value in env_vars.items():
            os.environ[key] = value
            
        # run docker-compose
        subprocess.Popen(docker_compose_cmd, stdout=None)


        # Connect to the Docker daemon
        client = docker.from_env()

        # Get the list of containers defined in the Docker Compose file
        while True:
            print("Monitoring containers")
            containers = client.containers.list()
            container_names = [container.name for container in containers]

            print(container_names)
            
            if 0 < len(container_names) < 3:
                print("test is finished")
                break             
            
            time.sleep(5)


        db_client = utils.connect_to_mongo()
        db = db_client["test"]
        collection = db["test"]

        num_docs = collection.count_documents({})
        recorded_packet_loss = utils.get_loss_from_doc(collection.find_one({}))
        lower_bound, upper_bound = utils.calculate_packetloss_bounds(
            packet_loss, duration, frequency
        )
        print("num_docs: ", num_docs)
        print("recorded_packet_loss: ", recorded_packet_loss)

        assert num_docs == 1
        assert lower_bound <= recorded_packet_loss <= upper_bound

    finally:
        # stop the containers
        utils.stop_containers()




if __name__ == "__main__":
    test_integration(1, 100, 10, 0, 100)