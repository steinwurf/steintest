[![GitHub release](https://img.shields.io/github/release/steinwurf/steintest.svg?color=blue)](https://github.com/steinwurf/steintest/releases/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?color=blue)](https://opensource.org/licenses/MIT)
[![GitHub All Releases](https://img.shields.io/github/downloads/steinwurf/steintest/total.svg?color=blue)](https://github.com/steinwurf/steintest/releases/)
![Go version](https://img.shields.io/badge/go-%3E%3D%201.18.1-blue.svg)

# Steintest

Steintest is a server and client tool written in Go that enables users to perform and document packetloss tests over a WebRTC connection (datachannel).

## Requirements

- Go version go1.18.1 linux/amd64
- Access to a MongoDB (connection string)

## Usage

1. Clone the repository: 

2. Start the server: 

To start the server, you will need to create a JSON file with the following format:

 ```
{
"port": "",
"dbconnectionstring" : "",
"collectionname": "",
"databasename" : "",
"servername" : ""
}
 ```

Replace the values with your own information, and save the file. The `servername` is what this server will be identified as in MongoDB.

Start the server by running:
 ```
<PathToServer> -json <PathToServerParams>
 ```

If "server running" is printed, the server is running and listening on the specified port.

3. Run the client:
 ```
 <PathToClient>
 ```

You can specify parameters for the test by passing command-line arguments. Use the following command to see the available parameters:
 ```
<PathToClient> -h
 ```

## Contributing
We welcome contributions to Steintest. If you would like to contribute, please fork the repository and create a pull request.

## Credits
Steintest uses the following open-source libraries:
- [pion/webrtc](https://github.com/pion/webrtc)
- [mongodb/mongo-go-driver](https://github.com/mongodb/mongo-go-driver)


## License
This project is licensed under the MIT License. See the LICENSE file for details.
