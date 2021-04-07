package main

import (
	"flag"
	"fmt"
)

func main() {
	var sourceFile = flag.String("source", "rss_feeds.json", "Feeds source")
	var destinationFile = flag.String("destination", "rss.json", "Destination file")
	var outputFormat = flag.String("format", "JSON", "Destination file format")
	var verboseMode = flag.Bool("verbose", false, "Enable output logging information")

	flag.Parse()

	fmt.Println(*sourceFile, *destinationFile, *outputFormat, *verboseMode)
}
