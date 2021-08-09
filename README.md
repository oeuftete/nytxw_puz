# NYT Crossword to Puz

Note: Running this script requires you're logged into nytimes.com in your browser.

To use:

```bash
nyt.py https://www.nytimes.com/crosswords/game/daily/2021/08/03 2021-08-03.puz
```

## TODO

* [ ] allow cookie file to be supplied directly
* [ ] use existing puz library (not sure if there any extra changes here to integrate)
* [ ] make it work, it doesn't for e.g. [the Aug. 21 bonus](https://www.nytimes.com/crosswords/game/bonus/2021/08).  This might be an XWord only thing, and using updated puz libs may help.
* [ ] use an existing lzstring library

## Mini FAQ

* What? Why?

The New York Times announced that on August 10th, [they will no longer
provide](https://www.nytimes.com/2021/08/02/crosswords/nyt-games-no-longer-available-on-across-lite-as-of-aug-9.html)
Across Lite .puz files for download.  This tool was made in response to that
decision, allowing users of that tool to continue to solve crossword puzzles in
their favorite program.

* Why not just use the NY Times app?

For me personally, I want something that works completely offline, and doesn't
require I stare at my phone even more.  I'm sure other people have other
reasons, so I decided to put my little tool online for others to use.

* Anything else?

Original author: [nobody514](https://www.reddit.com/user/nobody514/).
