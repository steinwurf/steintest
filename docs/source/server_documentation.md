# Server Documentation

The server listenes for http request on port 8080, it then upgrades the connectio to a websocket connection and when the client starts a test, it starts by creating a websocket connection to the server. when the connection is established and the client starts sending packets the server simply acts as an echo. When the test is finished the server sends the data and meta data to the database.


## Server.go
This file contains all the structs and functions used for the websocket server

`Run()`  
This function is the function that starts the server and make it listen for incoming connections on port 8080.
It calls `setupRoutes()`.  

`setupRoutes()`  
This function instantiate server struct, creating a pool of connections. This pool keeps track of the different websocket connections to users.  
This function also specifies that when an incoming http request is registered the `wsEndpoint` function is called.

`wsEndpoint(pool *Pool, w http.ResponseWriter, r *http.Request)`
This function is called when the server registeres an incoming http request. It serves multiple purposes:
- Creates the client object and registeres it in the pool.
- Upgardes the http request to a websocket connection.
- Calls the reader function.


`reader(client *Client, pool *Pool)`  
This function is the go routine running through out the connection. 
- Connects to the database.
- Created the webrtc connection and sets all the event listeners.
- Reading messages over the websocket, and calling the correct messages depending on the websocket      messages.



## webrtc.go
WIP

## database.go
WIP
