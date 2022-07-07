package src

import (
	"context"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const(
	dbconnectionstring = "mongodb+srv://NY-server:1IjA2u3W0rq5964g@db-mongo-81099e05.mongo.ondigitalocean.com/steintest?tls=true&authSource=admin&replicaSet=db-mongo"
)

func ConnectToDB() *mongo.Client {
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		panic(err)
	}
	err = client.Connect(context.TODO())
	if err != nil {
		panic(err)
	}
	return client
}
