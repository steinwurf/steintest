package main

import (
	"github.com/pion/webrtc/v3"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"strconv"
	"strings"
	"time"
)

type Packet struct {
	ID       int  `json:"id" bson:"id"`
	SentAt   int  `json:"sent_at" bson:"sent_at"`
	Received bool `json:"received" bson:"received"`
	RecvAt   int  `json:"recv_at" bson:"recv_at"`
	Latency  int  `json:"latency" bson:"latency"`
	Delayed  bool `json:"delayed" bson:"delayed"`
}

type MetaData struct {
	Frequency         int    `json:"frequency" bson:"frequency,omitempty"`
	Duration          int    `json:"duration" bson:"duration,omitempty"`
	AcceptableDelay   int    `json:"acceptable_delay" bson:"acceptable_delay,omitempty"`
	PacketSize        int    `json:"packet_size" bson:"packet_size,omitempty"`
	DestinationServer string `json:"destination_server" bson:"destination_server,omitempty"`
	Epoch             int    `json:"epoch" bson:"epoch,omitempty"`
}

type ClientData struct {
	IP        string `json:"ip" bson:"ip,omitempty"`
	UserAgent string `json:"user_agent" bson:"user_agent,omitempty"`
}

type TestData struct {
	ID         primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	RawData    []Packet           `bson:"raw_data,omitempty" json:"raw_data"`
	MetaData   MetaData           `bson:"meta_data,omitempty" json:"meta_data"`
	ClientData ClientData         `bson:"client_data,omitempty" json:"client_data"`
}
type DataFromClient struct {
	Type    string   `json:"type"`
	Payload TestData `json:"payload"`
}

func startTest(dc *webrtc.DataChannel, testParameters testParameters, client client) {
	NumberOfPackets := testParameters.Duration * testParameters.Frequency
	SleepTime := time.Duration(1000/testParameters.Frequency) * time.Millisecond
	InitialByteArray := make([]byte, testParameters.PacketSize)

	for i := 0; i < NumberOfPackets; i++ {
		packet_id := i

		packet := Packet{
			ID:       packet_id,
			SentAt:   int(time.Now().UnixMilli()),
			Received: false,
		}

		client.TestData.RawData = append(client.TestData.RawData, packet)

		copy(InitialByteArray, strconv.Itoa(packet_id))

		dc.Send(InitialByteArray)
		time.Sleep(SleepTime)
	}

	client.Webconn.WriteJSON(testStatusMsg{Type: "testStatus", Status: "finished"})

}

func recvData(msg webrtc.DataChannelMessage, client client) {
	decodedMsg := string(msg.Data)
	trimmed_msg := strings.Trim(decodedMsg, "\x00")

	decodedMsgInt, _ := strconv.Atoi(trimmed_msg)

	for i := range client.TestData.RawData {
		if client.TestData.RawData[i].ID == decodedMsgInt {
			client.TestData.RawData[i].RecvAt = int(time.Now().UnixMilli())
			client.TestData.RawData[i].Received = true
			client.TestData.RawData[i].Latency = client.TestData.RawData[i].RecvAt - client.TestData.RawData[i].SentAt
			if client.TestData.RawData[i].Latency > client.TestData.MetaData.AcceptableDelay {
				client.TestData.RawData[i].Delayed = true
			}
		}
	}
}
