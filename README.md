# What is Steintest? 
A packet loss measuring tool, measuring packet loss over webrtc connections.   

# Usage
This repository contains the code for running packloss tests over a webrtc connection. Visit website "steintest.steinwurf.com" if one wnats to test their connection to different servers.

If you want to run the program locally, you first need to start the server by running "main.go" it will start a server listening to the port 8080. 
Connecting to the server can happen through the GUI. To start the GIU run "index.html".

# Documentation
The documentation now is not greate but the overall logic will be added to the issue called documentation


# Developer
## Adding a new server 
* Create a Digital ocean droplet
* Add the IP of the droplet to the serverpicket on the frontend 
* Add the IP to trusted IPs on the mongodb cluster
* Create a MongoDB user for the server
* Updating the constants in the database.go
* clone this repo
* run main.go


## Updating the website
 * WIP



# License
This project is licensed under the MIT License - see the LICENSE.md file for details
