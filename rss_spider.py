#!/usr/bin/env python3
import argparse
import json
import os
import sys
from urllib import error, request
from xml.etree.ElementTree import parse


def create_default_source(filename: str) -> None:
    """
    Create RSS feed source examples into given file.
    """
    feeds = {
        "Planet Python": "https://planetpython.org/rss20.xml"
    }

    with open(filename, "w") as file:
        json.dump(feeds, file)


def fetch_parse_feeds(source: str, destination: str, limit: int) -> None:
    """
    Fetch RSS feed source and parse the content into destination according to
    the given limit of days.
    """
    request_headers = {"User-Agent": "Mozilla/5.0"}

    with open(source, "r") as file:
        rss_sources = json.load(file)

    for title, url in rss_sources.items():
        print("Accessing " + title)

        rss_request = request.Request(url, headers=request_headers)

        try:
            with request.urlopen(rss_request) as response:
                rss_doc = parse(response)

                for item in rss_doc.iterfind("channel/item"):
                    print("Title: " + item.findtext("title"))
                    print("Link: " + item.findtext("link") + "\n")

        except error.URLError as e:
            print(e.reason)


def read_robots() -> None:
    """
    Read from RSS feed robots.txt
    """
    pass


if __name__ == "__main__":
    """
    Main program entrypoint
    """
    # Command line parser
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-s", "--source", dest="source",
                            action="store", required=True,
                            default="rss_feeds.json",
                            help="RSS feed source, a default .rss_feeds.json \
                            will be created if not informed")

    arg_parser.add_argument("-d", "--destination", dest="destination",
                            action="store", required=False, default="/tmp/rss",
                            help="Destination directory, a default /tmp/rss \
                            will be created if not informed")

    arg_parser.add_argument("-l", "--limit", type=int, dest="limit",
                            action="store", required=False, default="1",
                            help="Limit the number of days to download. \
                            Default 1 (today)")

    args = arg_parser.parse_args()

    # Create an empty RSS feed source if the informed one does not exits
    if not os.path.isfile(args.source):
        print("Informed RSS feed source " + args.source +
              " does not exists, creating a default one." +
              " Fill this file and run again.")

        create_default_source(args.source)

        sys.exit()

    # Create destination directory if the informed one does not exits
    if not os.path.isdir(args.destination):
        print("Informed destination directory " + args.destination +
              " does not exists, creating.")

        os.mkdir(args.destination)

    # Fetch and parse from RSS feed sources based on the given limit of days
    # and save to destination directory
    fetch_parse_feeds(args.source, args.destination, args.limit)

    sys.exit()
