package src

import (
	"encoding/json"
	"fmt"
	"github.com/gorilla/websocket"
	"github.com/pion/webrtc/v3"
	"time"
)
type client struct {
	Webconn *websocket.Conn
	Pc *webrtc.PeerConnection
	TestData *testData
}

func Run(destinationParameters destinationParameters, testParameters testParameters) {
	client := client{TestData: &testData{}}

	client.Webconn = connectWebSocket(destinationParameters.Ip, destinationParameters.Port)

	client.Pc = createwebRTCConnection()

	defer deferfunc(client)


	client.TestData.MetaData = metaData{
		PacketSize: testParameters.PacketSize, 
		Duration: testParameters.Duration, 
		PacketsPerSecond: testParameters.PacketsPerSecond, 
		Date: time.Now().Format("2006-01-02 15:04:05"),
		FilePath: testParameters.FilePath,
	}

	dc := createDataChannel(client.Pc)

	setEventListeners(client, dc, testParameters)

	sendOffer(client.Pc, client.Webconn)

	for {
		_, p, err := client.Webconn.ReadMessage()
		if err != nil {
			panic(err)
		}
		var message map[string]interface{}
			json.Unmarshal(p, &message)


		switch message["type"]{

		case "answer":
			fmt.Println("Received answer")

			var answer webrtc.SessionDescription
			json.Unmarshal(p, &answer)
			
			client.Pc.SetRemoteDescription(answer)

		case "candidate":
			var candidateMsg candidateMsg	
			json.Unmarshal(p, &candidateMsg)

			candidate := webrtc.ICECandidateInit{Candidate: candidateMsg.Payload.Candidate, SDPMid: candidateMsg.Payload.SdpMid, SDPMLineIndex: candidateMsg.Payload.SdpMLineIndex}
			client.Pc.AddICECandidate(candidate)
		default:
			fmt.Println(string(p))
		}
	}
}

func deferfunc (client client){
	client.Webconn.Close()
	client.Pc.Close()
}


func connectWebSocket(ip string, port string) *websocket.Conn {
	fmt.Println("Connecting to websocket")

	conn, _, err := websocket.DefaultDialer.Dial("ws://" + ip + ":" + port, nil)
	if err != nil {
		fmt.Println("Failed to connect to websocket")
		panic(err)
	}
	fmt.Println("Connected to websocket")

	return conn
}

func createDataChannel(pc *webrtc.PeerConnection) *webrtc.DataChannel{
	dc, err := pc.CreateDataChannel("data", nil)
	if err != nil {
		panic(err)
	}

	return dc
}

func createwebRTCConnection() *webrtc.PeerConnection {
	// Create a new RTCPeerConnection
	configuration := webrtc.Configuration{
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
	pc, err := webrtc.NewPeerConnection(configuration)
	if err != nil {
		panic(err)
	}
	fmt.Println("Created webRTC connection")
	return pc
}

func sendOffer(pc *webrtc.PeerConnection, webconn *websocket.Conn) {
	offerMsg := offerMsg{}

	offer, err := pc.CreateOffer(nil)
	if err != nil {
		panic(err)
	}

	pc.SetLocalDescription(offer)

	offerMsg.Type = "offer"
	offerMsg.Payload = offer

	u, err := json.Marshal(offerMsg)
	if err != nil {
		panic(err)
	}
	webconn.WriteMessage(1, u)
}

// Handles the candidate from the client
func handleICECandidates(candidate *webrtc.ICECandidate, webconn *websocket.Conn, pc *webrtc.PeerConnection){
	if candidate != nil{

		object, err := json.Marshal(iceCandidate{Type:"candidate", Candidate:  candidate.ToJSON()})
		if err != nil {
			panic(err)
		}
		webconn.WriteMessage(1, object)
	}
}

func setEventListeners(client client, dc *webrtc.DataChannel, testParameters testParameters){
	
	client.Pc.OnICECandidate(func(candidate *webrtc.ICECandidate) {
		handleICECandidates(candidate, client.Webconn, client.Pc)
	})
	dc.OnOpen(func() {
		fmt.Println("Data channel opened")
		startTest(dc, testParameters, client)
	})
	dc.OnMessage(func(msg webrtc.DataChannelMessage) {
		recvData(msg, client)
	})

}

