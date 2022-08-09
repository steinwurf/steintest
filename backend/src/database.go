package src

import (
	"context"
	"encoding/json"
	"fmt"
	ua "github.com/mileusna/useragent"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)



type UserAgent struct{
	Name string `bson:"Name,omitempty"`
	Version string `bson:"Version,omitempty"`
	OS string `bson:"OS,omitempty"`
	OSVersion string  `bson:"OSVersion,omitempty"`
	Device string  `bson:"Device,omitempty"`
}

type SingleDataEntry struct{
	ID int`json:"id" bson:"id,omitempty"`
	SentAt int `json:"sentAt" bson:"sentAt,omitempty"`
	Recv bool `json:"recv" bson:"recv,omitempty"`
	RecvAt int `json:"recvAt" bson:"recvAt,omitempty"`
	Delay int `json:"delay" bson:"delay,omitempty"`
	Delayed bool `json:"delayed" bson:"delayed,omitempty"`
}

type TestData struct {
	ID primitive.ObjectID `bson:"_id,omitempty"`
	PacketData []SingleDataEntry `json:"PacketData" bson:"TestData,omitempty"`
	PacketLossPercentage float32 `json:"PacketLossPercentage" bson:"PacketLossPercentage"`
	ConsLostPacketData []int `json:"ConsLostPacketData" bson:"ConsLostPacketData"`
	Frequency int `json:"Frequency" bson:"Frequency,omitempty"`
	Duration int `json:"Duration" bson:"Duration,omitempty"`
	AcceptableDelay int `json:"AcceptableDelay" bson:"AcceptableDelay,omitempty"`
	IP string `json:"IP" bson:"IP,omitempty"`
	DestinationServer string `json:"DestinationServer" bson:DestinationServer",omitempty"`
	UserAgent UserAgent `json:"UserAgent" bson:"UserAgent,omitempty"`
	NumberOfPackets int `json:"NumberOfPackets" bson:"NumberOfPackets,omitempty"`
	TimeStamp int `json:"TimeStamp" bson:"TimeStamp,omitempty"`
	PacketSize int `json:"PacketSize" bson:"PacketSize,omitempty"`
	
}
type DataFromClient struct {
	Type string `json:"type"`
	Payload TestData `json:"payload"`
}



func ConnectToDB() *mongo.Client {
	client, err := mongo.NewClient(options.Client().ApplyURI(dbconnectionstring))
	if err != nil {
		panic(err)
	}
	err = client.Connect(context.TODO())
	if err != nil {
		panic(err)
	}
	return client
}
func InsertUA(TestData *TestData, client *Client){
	TestData.UserAgent = ParseUA(client.UserAgent)
}

func InsertData(data []byte, client *Client){


	DataFromClient := DataFromClient{}
	json.Unmarshal(data, &DataFromClient)

	// parse the ServerName to the object
	DataFromClient.Payload.DestinationServer = ServerName

	// insert the Ip form the client object

	DataFromClient.Payload.IP = client.IP

	// parse the useragent
	agent := ParseUA(client.UserAgent)

	DataFromClient.Payload.UserAgent = agent


	// insert the data into the database

	db := client.DBClient.Database(dataBaseName)
	coll := db.Collection(collectionName)

	_, err := coll.InsertOne(context.TODO(), DataFromClient.Payload)
    if err != nil {
        fmt.Println(err)
        return
    }
}




func ParseUA(UserAgentString string) UserAgent{

	ParsedObject := ua.Parse(UserAgentString)
	userAgent := UserAgent{
		Name: ParsedObject.Name,
		Version: ParsedObject.Version,
		OS: ParsedObject.OS,
		OSVersion: ParsedObject.OSVersion,
		Device: ParsedObject.Device,
	}

	return userAgent
}