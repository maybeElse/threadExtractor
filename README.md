# threadExtractor
a small python script for digesting twitter archives

## Usage:
1: download your twitter archive (settings->your account->download an archive). Expect to wait at least a day before the archive is available.
2: find `data/tweet.js`
3: remove `window.YTD.tweet.part0 = ` from the first line
4: save as `tweet.json` in the same directory as `threadExtractor.py`
5: run `threadExtrator.py`

## Flaws:
- At present, this script does not handle branching threads properly. Some tweets will be lost.
- Output text files are named based on the ID and time of the final tweet in each thread, instead of the initial one.
- While the script will attempt to strip numbering from tweets (eg trailing "y/" or "y/x"), this is imperfect.