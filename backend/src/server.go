package src

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"github.com/gorilla/websocket"
	"github.com/pion/webrtc/v3"
	"github.com/rs/xid"
	"strings"
	"go.mongodb.org/mongo-driver/mongo"
)

type Client struct{
	ID string
	SocketConn *websocket.Conn
	WebrtcConn *webrtc.PeerConnection
	DBClient *mongo.Client
	UserAgent string
	IP string
	TestData *TestData
}

type Server struct{
	Pool *Pool
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


func setEventListeners(client *Client){
	client.WebrtcConn.OnICECandidate(func(candidate *webrtc.ICECandidate) {
		handleICECandidates(candidate, *client)
	})

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
}

func reader(client *Client, pool *Pool){

	client.DBClient = ConnectToDB()
	fmt.Println("succesfully connected to db")

	defer func(){
		delete(pool.Clients, client)
		client.SocketConn.Close()
		fmt.Printf("client with id  %s has now left. %d users still connected \n", client.ID, len(pool.Clients))
	}()
	
	/* defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered. Error:\n", r)
        }
    }() */
	
	
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

	setEventListeners(client)

	for {
		// Read in a new message
		messageType, p, err := client.SocketConn.ReadMessage()
		if err != nil {
			log.Println(err)
			break	
		}


		//unmarshalling the message to a map
		var message map[string]interface{}
		json.Unmarshal(p, &message)

		switch message["type"]{

		case "offer":
			fmt.Println("offer received")
			var offerMsg offerMsg
			json.Unmarshal(p, &offerMsg)

			handleOffer(offerMsg, client.SocketConn, messageType, client.WebrtcConn)
		
		case "candidate":
			fmt.Println("candidate received")
			var candidateMsg candidateMsg	
			json.Unmarshal(p, &candidateMsg)

			candidate := webrtc.ICECandidateInit{Candidate: candidateMsg.Payload.Candidate, SDPMid: candidateMsg.Payload.SdpMid, SDPMLineIndex: candidateMsg.Payload.SdpMLineIndex}
			client.WebrtcConn.AddICECandidate(candidate)
		
		case "packetData":
			fmt.Println("recieved packet data")
			InsertData(p, client)
		
		case "testStatus":
			fmt.Println("test status received")
			client.SocketConn.WriteMessage(messageType, p)


		default:
			// THIS IS FOR DEBUGGING
			fmt.Println(string(p))

		}
	}
}

// The websocket endpoint
func wsEndpoint(pool *Pool, w http.ResponseWriter, r *http.Request){
	upgrader.CheckOrigin = func(r *http.Request) bool { return true}

	client := Client{
		ID: xid.New().String(), //Generating a random id for the client
		IP: strings.Split(r.RemoteAddr, ":")[0], // This line removes the port number from the ip
		UserAgent: r.UserAgent(), //Getting the user agent
	}
	
	pool.Clients[&client] = true


	var err error
	client.SocketConn, err = upgrader.Upgrade(w,r, nil)
	if err != nil{
		delete(pool.Clients, &client)
		panic(err)
	}

	
	log.Println("client succesfully connected to the server")
	go reader(&client, pool)

	defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered. Error:\n", r)
        }
    }()

}


func setupRoutes() {
	server := Server{Pool: NewPool()}
	
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		wsEndpoint(server.Pool, w, r)
	})

}

func Run() {
	fmt.Println("Starting server")
	setupRoutes()
	log.Fatal(http.ListenAndServe(":8080", nil))
}



