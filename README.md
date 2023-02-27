[![GitHub release](https://img.shields.io/github/release/steinwurf/steintest.svg)](https://github.com/steinwurf/steintest/releases/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub All Releases](https://img.shields.io/github/downloads/steinwurf/steintest/total.svg)](https://github.com/steinwurf/steintest/releases/)
[![Libraries.io](https://img.shields.io/librariesio/github/steinwurf/steintest.svg)](https://libraries.io/github/steinwurf/steintest)
![Go version](https://img.shields.io/badge/go-%3E%3D%201.18.1-blue.svg)

# What is Steintest? 
Steintest consists of a server and a client both written in golang. Steintests allow users to perform and document packetloss tests over a webrtc connection (datachannel).

# Requirements
This application is devopled with go version go1.18.1 linux/amd64 <br />
Access to a mongodb (connection string)


# Usage
Clone repository<br />
```git clone https://github.com/steinwurf/steintest.git``` <br />


# Server Setup 
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
<PathToServer> -json <PathToServerParams>
```
If "server running" is printed, the server is running and listening on the specified port.


# Client Setup

The client can be run by executing the executable: 
```
<PathToClient>
```

It is possible to specify the paramters for the test in the commandline, write 
```
<PathToClient> -h
```
To see the parameters.

# License
This project is under the MIT license 

