package main

import (
	"SteinTest/src"
	"fmt"
)


func main() {
	src.Run()
	client := src.ConnectToDB()
	fmt.Println(client)

}