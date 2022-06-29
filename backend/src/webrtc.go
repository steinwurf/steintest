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
	Candidate webrtc.ICECandidate `json:"candidate"` 
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
	pc.SetLocalDescription(answer)
	
	u, err := json.Marshal(answer)
	if err != nil {
		panic(err)
	}

	webconn.WriteMessage(msg_type, u)
}

func handleICECandidates(candidate *webrtc.ICECandidate, client Client){
	if candidate != nil{
		u, err := json.Marshal(iceCandidate{Type: "candidate", Candidate: *candidate})
		if err != nil {
			panic(err)
		}
		client.SocketConn.WriteMessage(1, u)
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