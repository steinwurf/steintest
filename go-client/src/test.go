package src

import(
	"fmt"
	"github.com/pion/webrtc/v3"
	"time"
	"strconv"
	"encoding/json"
	"io/ioutil"
	"bytes"
	"os"
)

type metaData struct {
	PacketSize int `json:"packetSize"`
	Duration int `json:"duration"`
	PacketsPerSecond int `json:"packetsPerSecond"`
	Date string `json:"date"`
	FilePath string `json:"filePath"`
}

type packet struct {
	ID string `json:"id"`
	SentAt time.Time `json:"sentAt"`
	ReceivedAt time.Time `json:"receivedAt"`
	Recv bool `json:"recv"`
}


type testData struct {
	MetaData metaData `json:"metaData"`
	TestDataArray []packet `json:"testDataArray"`
}


func startTest(dc *webrtc.DataChannel, testParameters testParameters, client client){
	fmt.Println("Starting test")
	NumberOfPackets := testParameters.Duration * testParameters.PacketsPerSecond
	SleepTime := time.Duration(1000/testParameters.PacketsPerSecond) * time.Millisecond
	InitialByteArray := make([]byte, testParameters.PacketSize)
	
	for i := 0; i < NumberOfPackets; i++{
		packet_id := strconv.Itoa(i)

		
		packet := packet{
			ID: packet_id, 
			SentAt: time.Now(), 
			Recv: false,
		}
		client.TestData.TestDataArray = append(client.TestData.TestDataArray, packet)
 
		copy(InitialByteArray[:], packet_id)
		
		dc.Send(InitialByteArray)
		time.Sleep(SleepTime)
	}
	fmt.Println("Test finished")
	
	// export the data
	exportData(client)

	os.Exit(0)
}

func recvData(msg webrtc.DataChannelMessage, client client){

	decodedMsg := bytes.Trim(msg.Data, "\x00")

	for i := range client.TestData.TestDataArray{
		if client.TestData.TestDataArray[i].ID == string(decodedMsg){

			client.TestData.TestDataArray[i].ReceivedAt = time.Now()
			client.TestData.TestDataArray[i].Recv = true
		}
	}
}

func exportData(client client){	
	// export the data
	
	fmt.Println("Exporting data")
	
	file, _ := json.MarshalIndent(client.TestData, "", " ")
 
	_ = ioutil.WriteFile(client.TestData.MetaData.FilePath, file, 0644)
}