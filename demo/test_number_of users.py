import subprocess
import atexit
import time


ip = "188.166.25.77"
duration = 30
clients = []

def spawn_client(number_of_clients):
    for i in range(number_of_clients):
        clients.append(subprocess.Popen(["./cli", "-Ip", f"{ip}", "-Duration", f"{duration}"]))

# Register an exit handler to terminate all child processes when the program exits
@atexit.register
def cleanup():
    for client in clients:
        client.terminate()


if __name__ == "__main__":
    print("Enter number of clients")
    number_of_clients = int(input())
    spawn_client(number_of_clients)
    time.sleep(duration + 10)