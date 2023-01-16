package main

import (
	"context"
	"encoding/json"
	"fmt"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

)

type Packet struct{
	ID int`json:"id" bson:"id"`
	SentAt int `json:"sent_at" bson:"sent_at"`
	Received bool `json:"received" bson:"received"`
	RecvAt int `json:"recv_at" bson:"recv_at"`
	Latency int `json:"latency" bson:"latency"`
	Delayed bool `json:"delayed" bson:"delayed"`
}

type MetaData struct {
	Frequency int `json:"frequency" bson:"frequency,omitempty"`
	Duration int `json:"duration" bson:"duration,omitempty"`
	AcceptableDelay int `json:"acceptable_delay" bson:"acceptable_delay,omitempty"`
	PacketSize int `json:"packet_size" bson:"packet_size,omitempty"`
	DestinationServer string `json:"destination_server" bson:"destination_server,omitempty"`
	Epoch int `json:"epoch" bson:"epoch,omitempty"`
}

type ClientData struct {
	IP string `json:"ip" bson:"ip,omitempty"`
	UserAgent string `json:"user_agent" bson:"user_agent,omitempty"`
}

type TestData struct {
	ID primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	RawData []Packet `bson:"raw_data,omitempty" json:"raw_data"`
	MetaData MetaData `bson:"meta_data,omitempty" json:"meta_data"`
	ClientData ClientData `bson:"client_data,omitempty" json:"client_data"`
}
type DataFromClient struct {
	Type string `json:"type"`
	Payload TestData `json:"payload"`
}



func ConnectToDB(dbconnectionstring string) *mongo.Client {
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

func InsertData(data []byte, client *Client, serverParams *ServerParams){

	DataFromClient := DataFromClient{}
	json.Unmarshal(data, &DataFromClient)

	// parse the ServerName to the object
	DataFromClient.Payload.MetaData.DestinationServer = serverParams.ServerName

	// insert the Ip form the client object

	DataFromClient.Payload.ClientData.IP = client.IP

	// insert the user agent from the client object
	DataFromClient.Payload.ClientData.UserAgent = client.UserAgent

	// insert the data into the database

	db := client.DBClient.Database(serverParams.DatabaseName)
	coll := db.Collection(serverParams.CollectionName)

	_, err := coll.InsertOne(context.TODO(), DataFromClient.Payload)
    if err != nil {
        fmt.Println(err)
        return
    }
	fmt.Println("succesfully inserted data")
}
