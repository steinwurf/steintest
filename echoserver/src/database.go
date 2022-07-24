package src

import (
	"context"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"fmt"
	"encoding/json"
	ua "github.com/mileusna/useragent"
)

const(
	
	dbconnectionstring = "mongodb+srv://NY-server:6mc5Y0lVj2z1934K@db-mongo-81099e05.mongo.ondigitalocean.com/steintest?tls=true&authSource=admin&replicaSet=db-mongo"
	collectionName = "sessiondata"
	dataBaseName = "steintest"
	ServerName = "New York"

)

type UserAgent struct{
	Name string `bson:"Name,omitempty"`
	Version string `bson:"Version,omitempty"`
	OS string `bson:"OS,omitempty"`
	OSVersion string  `bson:"OSVersion,omitempty"`
	Device string  `bson:"Device,omitempty"`
}

type SingleDataEntry struct{
	Id int`json:"id" bson:"id,omitempty"`
	SentAt int `json:"sentAt" bson:"sentAt,omitempty"`
	Recv bool `json:"recv" bson:"recv,omitempty"`
	RecvAt int `json:"recvAt" bson:"recvAt,omitempty"`
	Delay int `json:"delay" bson:"delay,omitempty"`
	Delayed bool `json:"delayed" bson:"delayed,omitempty"`
}

type TestData struct {
	ID primitive.ObjectID `bson:"_id,omitempty"`
	TestData []SingleDataEntry `bson:"TestData,omitempty"`
	NumberOfPacketSent int `bson:"NumberOfPacketSent,omitempty"`
	PacketLossPercent int `bson:"PacketLossPercent,omitempty"`
	IP string `bson:"IP,omitempty"`
	DestinationServer string `bson:DestinationServer",omitempty"`
	UserAgent UserAgent `bson:"UserAgent,omitempty"`
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

func InsertData(data []byte, client *Client){
	// parse the useragent
	agent := ParseUA(client.UserAgent)

	db := client.DBClient.Database(dataBaseName)
	coll := db.Collection(collectionName)

	testData := TestData{
		UserAgent: agent,
		DestinationServer: ServerName,
		IP: client.IP ,
	}
	
	var dataEntries []SingleDataEntry
	json.Unmarshal(data, &dataEntries)

	testData.TestData = dataEntries

	_, err := coll.InsertOne(context.TODO(), testData)
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