# What is Steintest? 
A packet loss measuring tool, measuring packet loss over webrtc connections.

# Usage

## DOCKER
Retrieve both the server and go-client images from ... (Insert dockerhub link here)
The docker version is not fully functioning. 

WIP :construction_worker: :construction_worker: :construction_worker: 



## GO BINARIES
The package is developed in go version 1.18.1. 

 - Clone the repository
 - Starting the server
    - In the /backend folder run: 
    ```bash
        go mod download
        go run main.go
    ```
    You should get a message showing that the server has started 
 - connecting a client
    - in the /go-client folder run:
    ```bash
        go mod download
        go run main.go
    ```
    You should now see that the client has connected to the server and they are running the test.
    The log file of the test is stored in the /logs folder. 
    
    





# Documentation
The documentation now is limited but the overall logic will be added to the issue called documentation



# License
The license of this project is unkown.
