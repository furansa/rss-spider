package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

func fetchFeedsData(feedsSourceFile *os.File) error {
	file, err := os.Open(feedsSourceFile.Name())

	if err != nil {
		return err
	}

	fmt.Println(file.Name())

	return nil
}

func formatFeedsData() {
}

func main() {
	var sourceFile = flag.String("source", "rss_feeds.json", "Feeds source")
	var destinationFile = flag.String("destination", "rss.json", "Destination file")
	var outputFormat = flag.String("format", "JSON", "Destination file format")
	var verboseMode = flag.Bool("verbose", false, "Enable output logging information")

	flag.Parse()

	if *verboseMode {
		log.Printf("Logging enabled")
	}

	fmt.Println(*sourceFile, *destinationFile, *outputFormat, *verboseMode)
}
