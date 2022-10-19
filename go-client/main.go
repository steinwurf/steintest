package main

import (
	"go-client/src"
)


func main() {
	destinationParameters, testParameters := src.Cli()

	src.Run(destinationParameters, testParameters)
		}