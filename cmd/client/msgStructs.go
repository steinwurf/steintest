package main	

import (
	"github.com/pion/webrtc/v3"
)


type sdpPayload struct {
	Sdp string `json:"sdp"`
	Type string `json:"type"`
}

type offerMsg struct{
	Type string `json:"type"`
	Payload webrtc.SessionDescription `json:"Payload"`
}

type iceCandidate struct{
	Type string `json:"type"`
	Candidate webrtc.ICECandidateInit `json:"candidate"` 
}


type candidatePayLoad struct {
	Candidate string `json:"candidate"`
	SdpMid *string `json:"sdpMid"`
	SdpMLineIndex *uint16 `json:"sdpMLineIndex"`
}

type candidateMsg struct {
	Type string `json:"type"`
	Payload candidatePayLoad `json:"candidate"`
}

type testStatusMsg struct {
	Type string `json:"type"`
	Status  string `json:"payload"`
}