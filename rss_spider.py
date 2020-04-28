#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime
from typing import List
from urllib.error import URLError
from urllib.request import Request, urlopen
from xml.etree.ElementTree import parse


def create_default_source(filename: str) -> None:
    """
    Create RSS feed source examples into given file.

    :param filename: Name of the source file
    :type filename: str

    :return: None
    :rtype: None
    """
    feeds = {
        "Planet Python": "https://planetpython.org/rss20.xml",
        "Real Python": "https://realpython.com/atom.xml",
        "Schneier on Security": "https://www.schneier.com/blog/atom.xml"
    }

    with open(filename, "w") as file:
        json.dump(feeds, file)


# TODO: Implement limit logic
def fetch_feeds(source: str, limit: int) -> List:
    """
    Fetch RSS feed source according to the given limit of days.

    :param source: Name of the source file
    :type source: str

    :param limit: Limit of days to fetch
    :type limit: int

    :return: RSS feed names and content
    :rtype: List
    """
    request_headers = {"User-Agent": "Mozilla/5.0"}
    request_timeout = 10
    rss_data = list()

    # Read the RSS feed sources
    with open(source, "r") as file:
        rss_sources = json.load(file)

    # For each RSS source
    for name, url in rss_sources.items():
        rss_request = Request(url, headers=request_headers)

        try:
            with urlopen(rss_request, timeout=request_timeout) as response:
                # Parse response and append to a list with RSS feed name
                rss_response = parse(response)
                rss_data.append((name, rss_response))

        except URLError as e:
            print(e.reason)

    return rss_data


# TODO: Sort by category
def format_data(rss_data: List, filename: str) -> None:
    """
    Format and structure data into final document.

    :param rss_data: RSS feed name and content
    :type rss_data: List

    :param filename: Name of the destination file
    :type filename: str

    :return: None
    :rtype: None
    """
    timestamp = datetime.now()

    with open(filename, "w") as file:
        file.write("# News\nLast update: " + str(timestamp) + ".\n")

        for name, data in rss_data:
            file.write("\n## " + name + "\n")
            # TODO: Optimize it
            # Format and write data based on http://www.w3.org/2005/Atom
            atom_prefix = "{http://www.w3.org/2005/Atom}"
            for item in data.iterfind(atom_prefix + "entry"):
                file.write("* [" + item.findtext(atom_prefix +
                           "title") + "](" +
                           item.find(atom_prefix +
                           "link").attrib["href"] + ")\n")

            # Format data and write based on http://purl.org/dc/elements/1.1/
            for item in data.iterfind("channel/item"):
                file.write("* [" + item.findtext("title") + "](" +
                           item.findtext("link") + ")\n")


# TODO
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
    rss_data = fetch_feeds(args.source, args.limit)

    # Format and save RSS data
    filename = args.destination + "/news.md"
    format_data(rss_data, filename)

    sys.exit()
