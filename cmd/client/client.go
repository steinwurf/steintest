package main

import (
	"encoding/json"
	"fmt"
	"github.com/gorilla/websocket"
	"github.com/pion/webrtc/v3"
	"log"
	"net"
	"os"
	"time"
)

type client struct {
	Webconn  *websocket.Conn
	Pc       *webrtc.PeerConnection
	TestData *TestData
}

func Run(destinationParameters destinationParameters, testParameters testParameters) {
	client := client{TestData: &TestData{}}

	client.Webconn = connectWebSocket(destinationParameters.Ip, destinationParameters.Port)

	client.Pc = createwebRTCConnection()

	defer deferfunc(client)

	client.TestData.MetaData = MetaData{
		AcceptableDelay:   testParameters.AcceptableDelay,
		DestinationServer: destinationParameters.Ip,
		PacketSize:        testParameters.PacketSize,
		Duration:          testParameters.Duration,
		Frequency:         testParameters.Frequency,
		Epoch:             int(time.Now().Unix() * 1000),
	}

	client.TestData.ClientData = ClientData{
		IP:        GetOutboundIP().String(),
		UserAgent: "go-client",
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

		switch message["type"] {

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

		case "testStatus":
			client.Webconn.WriteJSON(DataFromClient{Payload: *client.TestData, Type: "packetData"})
			os.Exit(deferfunc(client))

		default:
			fmt.Println("The string did not did not match any of the cases")
		}
	}
}

func deferfunc(client client) int {
	fmt.Println("Closing connections")
	client.Webconn.Close()
	client.Pc.Close()
	return 0
}

func connectWebSocket(ip string, port string) *websocket.Conn {
	fmt.Println("Connecting to websocket")

	conn, _, err := websocket.DefaultDialer.Dial("ws://"+ip+":"+port, nil)
	if err != nil {
		fmt.Println("Failed to connect to websocket")
		fmt.Println("Make sure that the backend is running and listening on the correct addres eg.", ip, ":", port)
		os.Exit(0)
	}
	fmt.Println("Connected to websocket")

	return conn
}

func createDataChannel(pc *webrtc.PeerConnection) *webrtc.DataChannel {
	falseBool := false
	var maxRetransmits uint16 = 0

	options := webrtc.DataChannelInit{
		Ordered:        &falseBool,
		MaxRetransmits: &maxRetransmits,
	}

	dc, err := pc.CreateDataChannel("data", &options)
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
				URLs:       []string{"turn:142.93.235.90:3478"},
				Username:   "test",
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
func handleICECandidates(candidate *webrtc.ICECandidate, webconn *websocket.Conn, pc *webrtc.PeerConnection) {
	if candidate != nil {

		object, err := json.Marshal(iceCandidate{Type: "candidate", Candidate: candidate.ToJSON()})
		if err != nil {
			panic(err)
		}
		webconn.WriteMessage(1, object)
	}
}

func setEventListeners(client client, dc *webrtc.DataChannel, testParameters testParameters) {

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

// Get preferred outbound ip of this machine
func GetOutboundIP() net.IP {
	conn, err := net.Dial("udp", "8.8.8.8:80")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	localAddr := conn.LocalAddr().(*net.UDPAddr)

	return localAddr.IP
}
