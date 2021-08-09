#!/usr/bin/env python3

import html
import json
import os
import re
import sys

import browser_cookie3
import requests

import decompress
import puz

CACHE_DATA = False

BLOCK_LEFT = "\u2590"
BLOCK_MID = "\u2588"
BLOCK_RIGHT = "\u258c"
TITLE_LINE = "\u2501"


def get_puzzle(url):
    cache = {}
    if CACHE_DATA:
        # Simple cache, useful for debugging, grows to stupid
        # size over time, so it's off generally
        if os.path.isfile(".cached.json"):
            with open(".cached.json", "r", encoding="utf-8") as f:
                cache = json.load(f)

    if url not in cache:
        print(f"Loading {url}...")
        # Pull out the nytimes cookies from the user's browser
        cookies = browser_cookie3.chrome(domain_name="nytimes.com")
        # Load the webpage, its inline javascript includes the puzzle data
        resp = requests.get(url, cookies=cookies).content
        resp = resp.decode("utf-8")
        # Look for the javascript, it's easist here to just use a regex
        m = re.search(
            "(pluribus|window.gameData) *= *['\"](?P<data>.*?)['\"]", resp)
        # Pull out the data element
        resp = m.group("data")
        # Which is url-encoded
        resp = decompress.decode(resp)
        # And LZString compressed
        resp = decompress.decompress(resp)
        # And a JSON blob
        resp = json.loads(resp)
        cache[url] = resp
        if CACHE_DATA:
            with open(".cached.json", "w", newline="", encoding="utf-8") as f:
                json.dump(cache, f)

    return cache[url]


def data_to_puz(puzzle):
    p = puz.Puzzle()
    data = puzzle["gamePageData"]
    # Basic header
    p.title = "New York Times Crossword"
    p.author = ", ".join(data["meta"]["constructors"])

    # Pull out the size of the puzzle
    p.height = data["dimensions"]["rowCount"]
    p.width = data["dimensions"]["columnCount"]

    # Fill out the main grid
    p.solution = "".join(
        [x["answer"][0] if "answer" in x else "." for x in data["cells"]]
    )
    p.fill = "".join(["-" if "answer" in x else "." for x in data["cells"]])

    # And the clues, they're HTML text here, so decode them
    p.clues = [html.unescape(x["text"]) for x in data["clues"]]

    # See if any of the answers is multi-character (rebus)
    if max([len(x["answer"]) for x in data["cells"] if "answer" in x]) > 1:
        # We have at least one rebus answer, so setup the rebus data fields
        rebus = p.create_empty_rebus()

        # And find all the rebus answers and add them to the data
        for cell in data["cells"]:
            if "answer" in cell and len(cell["answer"]) > 1:
                rebus.add_rebus(cell["answer"])
            else:
                rebus.add_rebus(None)

    # All done
    return p


def main():
    if len(sys.argv) == 3:
        url, output_fn = sys.argv[1:3]
    else:
        url = input("Enter the NY Times crossword URL: ")
        output_fn = input("Enter the output filename: ")

    # Get the puzzle from NYT, the first time this is called
    # the cookie will be archived
    puzzle = get_puzzle(url)

    # And turn the puzzle data from NYT into a puz data structure
    output = data_to_puz(puzzle)
    output.save(output_fn)
    print(f"Created {output_fn}")


if __name__ == "__main__":
    main()
