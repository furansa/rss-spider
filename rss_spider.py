#!/usr/bin/env python3
import argparse
import json
import os
import sys


def create_default_source(filename: str) -> None:
    """Create RSS feed source examples into given file."""
    feeds = {
        "My Feed": "http://myfeed.com/rss",
        "Another Feed": "http://anotherfeed.com/rss",
        "Third Feed": "http://thirdfeed.com/rss",
    }

    with open(filename, "w") as file:
        json.dump(feeds, file)


if __name__ == "__main__":
    """Main program"""
    # Command line parser
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-s", "--source", dest="source",
                            action="store", required=True,
                            default="rss_feeds.json",
                            help="RSS feed source, a default .rss_feeds.json \
                            will be created if not informed")

    arg_parser.add_argument("-d", "--destination", dest="destination",
                            action="store", required=False, default="/tmp/rss",
                            help="Destination path, a default /tmp/rss will be \
                            created if not informed")

    arg_parser.add_argument("-l", "--limit", dest="limit", action="store",
                            required=False, default="1", help="Limit the number \
                            of days to download. Default 1 (today)")

    args = arg_parser.parse_args()

    # Create an empty RSS feed source if the informed one does not exits
    if not os.path.isfile(args.source):
        print("Informed RSS feed source " + args.source +
              " does not exists, creating a default one." +
              " Fill this file and run again.")

        create_default_source(args.source)

        sys.exit()

    # Create destination path if the informed one does not exits
    if not os.path.isdir(args.destination):
        print("Informed destination path " + args.destination +
              " does not exists, creating.")

        os.mkdir(args.destination)

    sys.exit()
