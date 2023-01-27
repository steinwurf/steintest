
# :construction_worker: :construction_worker: WIP :construction_worker: :construction_worker:

# What is Steintest? 
Steintest consists of a server and a client both written in golang. Steintests allow users to perform and document packetloss tests over a webrtc connection (datachannel). 

# requirements
This application is devopled with go version go1.18.1 linux/amd64 <br />
Access to a mongodb (connection string)


# Usage
Clone repository<br />
```git clone https://github.com/steinwurf/steintest.git``` <br />


# Server setup 
For the server to function it needs a json file with the following format
```
{
    "port": "",
    "dbconnectionstring" : "",
    "collectionname": "",
    "databasename" : "",
    "servername" : ""
}

```
The ServerName is simply what this server is identified as in the mongodb. <br />

This file must be passed to the server when running it.

Now the server is ready to be started: 
```
./cmd/server/server -json <PathToServerParams>
```
If "server running" is printed, the server is running and listening on the specified port.


# client setup

The client can be run by executing the executable: 
```
./cmd/client/client
```

It is possible to specify the paramters for the test in the commandline, write 
```
./cmd/client/client -h
```
To see the parameters.

# License
This project is under the MIT license 

