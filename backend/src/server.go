package src

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/websocket"
	"github.com/pion/webrtc/v3"
	"github.com/rs/xid"
	"sync"
)

type Client struct{
	ID string
	SocketConn *websocket.Conn
	WebrtcConn *webrtc.PeerConnection
}

type Server struct{
	Pool *Pool
	Mutex sync.Mutex
}


type Pool struct{
	Clients map[*Client]bool
}

func NewPool() *Pool {
	return &Pool{
		Clients: make( map[*Client]bool),
	}
}


var upgrader = websocket.Upgrader{
	ReadBufferSize: 1024,
	WriteBufferSize: 1024,
}

func reader(client *Client, pool *Pool){

	defer func(){
		delete(pool.Clients, client)
		client.SocketConn.Close()
		fmt.Printf("client with id  %s has now left. %d users still connected \n", client.ID, len(pool.Clients))
	}()

	config := webrtc.Configuration{
		ICEServers: []webrtc.ICEServer{
			{
				URLs: []string{"stun:stun1.l.google.com:19302"},
			},
			{
				URLs: []string{"turn:142.93.235.90:3478"},
				Username: "test",
				Credential: "test123",
			},
		},
	}

	var err error
	client.WebrtcConn, err = webrtc.NewPeerConnection(config)
	if err != nil {
		panic(err)
	}

	// event handler for icecandidates
	client.WebrtcConn.OnICECandidate(func(candidate *webrtc.ICECandidate) {
			handleICECandidates(candidate, *client)
	})
	// event handler for opening a datachannel
	client.WebrtcConn.OnDataChannel(func(dc *webrtc.DataChannel) {
			handleOpenDataChannel(dc, *client)
	})

	client.WebrtcConn.OnConnectionStateChange(func(state webrtc.PeerConnectionState) {
		onConnectionStateChange(state)
	})

	client.WebrtcConn.OnICEConnectionStateChange(func (state webrtc.ICEConnectionState)  {
		onICEConnectionStateChange(state)
	})

	client.WebrtcConn.OnICEGatheringStateChange(func (state webrtc.ICEGathererState)  {
		onICEGatheringStateChange(state)
	})

	client.WebrtcConn.OnNegotiationNeeded(func ()  {
		onNegotiationNeeded()
	})

	client.WebrtcConn.OnSignalingStateChange(func (state webrtc.SignalingState)  {
		onSignalingStateChange(state)
	})


	for {
		messageType, p, err := client.SocketConn.ReadMessage()
		if err != nil {
			log.Println(err)
			return
		}

		// It is a offer:
		if string(p)[9:14] == "offer"{
			var offerMsg offerMsg	
			json.Unmarshal(p, &offerMsg)
			fmt.Println("offer:")
			fmt.Println(offerMsg)
			handleOffer(offerMsg, client.SocketConn, messageType, client.WebrtcConn)
		}

		//its a candidate:
		if string(p)[9:18] == "candidate"{
			var candidateMsg candidateMsg	
			json.Unmarshal(p, &candidateMsg)

			candidate := webrtc.ICECandidateInit{Candidate: candidateMsg.Payload.Candidate, SDPMid: candidateMsg.Payload.SdpMid, SDPMLineIndex: candidateMsg.Payload.SdpMLineIndex}
			fmt.Println("remote ice candidates")
			fmt.Println(candidate)
			client.WebrtcConn.AddICECandidate(candidate)
		}
	}
}


func wsEndpoint(pool *Pool, w http.ResponseWriter, r *http.Request){
	upgrader.CheckOrigin = func(r *http.Request) bool { return true}

	client := Client{
		ID: xid.New().String(),
	}

	pool.Clients[&client] = true

	var err error
	client.SocketConn, err = upgrader.Upgrade(w,r, nil)
	if err != nil{
		log.Println(err)
	}

	log.Println("client succesfully connected to the server")
	go reader(&client, pool)
}


func setupRoutes() {
	server := Server{Pool: NewPool(), Mutex: sync.Mutex{}}
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		wsEndpoint(server.Pool, w, r)
	})

}

func Run() {
	fmt.Println("Starting server")
	setupRoutes()
	log.Fatal(http.ListenAndServe(":8080", nil))
}


