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
For the server to insert the data in the mongodb a file with following format must be provided. <br />
It must be saved as /cmd/server/ServerInfo.go.
```
package main 

const(
	dbconnectionstring = "" 
	collectionName = ""
	dataBaseName = ""
	ServerName = ""
)
```
The ServerName is simply what this server is identified as in the mongodb. <br />

Now the server is ready to be started: 
```
./cmd/server/server
```
If "server running" is printed, the server is running and listening on port 8080


# client setup

The client can be run by executing the executable: 
```
./cmd/client/client
```

It is possible to specify the paramters for the test by..



# License
This project is under the MIT license 
