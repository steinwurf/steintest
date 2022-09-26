package src

import (
	"context"
	"encoding/json"
	"fmt"
	ua "github.com/mileusna/useragent"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"io/ioutil"
	"log"
	"net/http"
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

type GeoLocation struct{
	Latitude float64 `json:"latitude" bson:"latitude,omitempty"`
	Longitude float64 `json:"longitude" bson:"longitude,omitempty"`
	ContinentCode string `json:"continent_code" bson:"continentCode,omitempty"`
	ContinentName string `json:"continent_name" bson:"continentName,omitempty"`
	CountryCode string `json:"country_code" bson:"countryCode,omitempty"`
	CountryName string `json:"country_name" bson:"countryName,omitempty"`
	RegionCode string `json:"region_code" bson:"regionCode,omitempty"`
	RegionName string `json:"region_name" bson:"regionName,omitempty"`
	City string `json:"city" bson:"city,omitempty"`
	Zip string `json:"zip" bson:"zip,omitempty"`
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
	GeoLocation GeoLocation `json:"GeoLocation" bson:"GeoLocation,omitempty"`
	
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

func GetGeoLocation(IP string) GeoLocation{
	geoLocation := GeoLocation{}
	access_key := "e3631a7fc4c9876e92eb5df03fa621c4";

	resp, err := http.Get("http://api.ipapi.com/" + IP + "?access_key=" + access_key)
	if err != nil {
	   log.Fatalln(err)
	}
 //We Read the response body on the line below.
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
	   log.Fatalln(err)
	}

	err = json.Unmarshal(body, &geoLocation)
	return geoLocation
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

	// parse the ip to geolocation
	geolocation := GetGeoLocation(client.IP)

	DataFromClient.Payload.GeoLocation = geolocation
	

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