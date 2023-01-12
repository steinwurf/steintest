package main

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
	Frequency int `default:"150"`
	AcceptableDelay int `default:"100"`
}

func Cli() (destinationParameters, testParameters) {
	Ip := flag.String("Ip", "localhost", "The ip address of the server")
	Port := flag.String("Port", "8080", "the port of the server")
	PacketSize := flag.Int("PacketSize", 1024, "the size of the packet")
	Duration := flag.Int("Duration", 10, "the duration of the test in seconds")
	Frequency := flag.Int("Frequency", 150, "the frequency in Hz")
	AcceptableDelay := flag.Int("AcceptableDelay", 150, "the acceptable delay in ms")
	
	flag.Parse()

	return destinationParameters{*Ip, *Port}, testParameters{*PacketSize, *Duration, *Frequency, *AcceptableDelay}

}