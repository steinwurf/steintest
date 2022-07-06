package src

import (
	"encoding/json"
	"fmt"

	"github.com/gorilla/websocket"
	"github.com/pion/webrtc/v3"
)


type sdpPayload struct {
	Sdp string `json:"sdp"`
	Type string `json:"type"`
}

type offerMsg struct{
	Type string `json:"type"`
	Payload sdpPayload `json:"Payload"`

}

type offerPayLoad struct {
	Candidate string `json:"candidate"`
	SdpMid *string `json:"sdpMid"`
	SdpMLineIndex *uint16 `json:"sdpMLineIndex"`
}

type candidateMsg struct {
	Type string `json:"type"`
	Payload offerPayLoad `json:"Payload"`
}

type webSocketConnection struct{
	conn *websocket.Conn 
}

type iceCandidate struct{
	Type string `json:"type"`
	Candidate webrtc.ICECandidateInit `json:"candidate"` 
}

func handleOffer (offerMsg offerMsg, webconn *websocket.Conn, msg_type int, pc *webrtc.PeerConnection){

	sdp_type := webrtc.NewSDPType(offerMsg.Payload.Type)
	remote := webrtc.SessionDescription{Type: sdp_type, SDP: offerMsg.Payload.Sdp}


	if err := pc.SetRemoteDescription(remote); err != nil{
		panic(err)
	}

	answer, err := pc.CreateAnswer(nil)
	if err != nil{
		panic(err)
	}
	fmt.Println("Answer:")
	fmt.Println(answer)
	fmt.Println("local description is set")
	pc.SetLocalDescription(answer)
	
	u, err := json.Marshal(answer)
	if err != nil {
		panic(err)
	}

	webconn.WriteMessage(msg_type, u)
}

func handleICECandidates(candidate *webrtc.ICECandidate, client Client){
	fmt.Println("our Icecandidate")
	if candidate != nil{

/* 		u, err := json.Marshal(iceCandidate{Type: "candidate", Candidate: *candidate})
		if err != nil {
			panic(err)
		} */

		object, err := json.Marshal(iceCandidate{Type:"candidate", Candidate:  candidate.ToJSON()})
		if err != nil {
			panic(err)
		}
		client.SocketConn.WriteMessage(1, object)
	}
}

func handleMessageDataChannel(msg webrtc.DataChannelMessage, client Client, channel *webrtc.DataChannel ){
	channel.Send(msg.Data)
	fmt.Println(string(msg.Data))
}

func handleOpenDataChannel(channel *webrtc.DataChannel, client Client){
	channel.OnMessage(func(msg webrtc.DataChannelMessage) {
		handleMessageDataChannel(msg, client, channel)
	},
)
}

func  onConnectionStateChange(state webrtc.PeerConnectionState){
	fmt.Println("PeerConnectionState is ", state)
}

func onICEConnectionStateChange(state webrtc.ICEConnectionState){
	fmt.Println("ConnectionState is ", state)
}

func onICEGatheringStateChange(state webrtc.ICEGathererState){
	fmt.Println("GatheringState is ", state)
}

func onNegotiationNeeded(){
	fmt.Println("Negotiation is needed")
}

func onSignalingStateChange(state webrtc.SignalingState){
	fmt.Println("SignalingState is ", state)
}
