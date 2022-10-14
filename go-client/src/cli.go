package src

import (
	"flag"
)

type destinationParameters struct {
	Ip string `default:"localhost"`
	Port string `default:"8080"`
}

type testParameters struct {
	PacketSize int `default:"1024"`
	Duration int `default:"10"`
	PacketsPerSecond int `default:"150"`
	FilePath string `default:"TestData.json"`
}

func Cli() (destinationParameters, testParameters) {
	Ip := flag.String("Ip", "localhost", "The ip address of the server")
	Port := flag.String("Port", "8080", "the port of the server")
	PacketSize := flag.Int("PacketSize", 1024, "the size of the packet")
	Duration := flag.Int("Duration", 10, "the duration of the test in seconds")
	PacketsPerSecond := flag.Int("PacketsPerSecond", 150, "the frequency of the packets per seconds")
	FilePath := flag.String("FilePath", "TestData.json", "the path to the file to be sent")

	flag.Parse()

	return destinationParameters{*Ip, *Port}, testParameters{*PacketSize, *Duration, *PacketsPerSecond, *FilePath}

}