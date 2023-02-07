package main


import (
	"flag"
	"fmt"
	"os"
	"encoding/json"
	"io/ioutil"
)

type ServerParams struct {
	Port string `json:"port" default:"8080"`
	DbConnectionString string `json:"dbconnectionstring"`
	CollectionName string `json:"collectionname"`
	DatabaseName string `json:"databasename"`
	ServerName string `json:"servername"`
}



func Cli() ServerParams {
	
	// define the flag
    jsonFile := flag.String("serverParams", "", "a JSON file containing the server parameters, find an example in the repo")

    // parse the flags
    flag.Parse()

	// check if the flag was provided
    if *jsonFile == "" {
        fmt.Println("error: please provide a JSON file using the -json flag the json file should contain the meta data about the server")
        os.Exit(1)
    }

	// open the file
    file, err := os.Open(*jsonFile)
    if err != nil {
        fmt.Printf("error: %v\n", err)
        os.Exit(1)
    }
    
	// close the file
	defer file.Close()

	// read the file
	file1, err := ioutil.ReadFile(*jsonFile)

	// unmarshal the file
	serverparams := ServerParams{}

	err = json.Unmarshal(file1, &serverparams)

	return serverparams
}