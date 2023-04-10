# threadExtractor
a small python script for digesting twitter archives

## Usage:
1. download your twitter archive (settings->your account->download an archive). Expect to wait at least a day before the archive is available.
2. find `data/tweet.js`
3. remove `window.YTD.tweet.part0 = ` from the first line
4. save as `tweet.json` in the same directory as `threadExtractor.py`
5. run `threadExtrator.py`

this script offers three modes:
- \[S\]earch: It can attempt to find *every* thread in your twitter archive and export them as text files.
- \[H\]unt: Given the id of the last tweet in a thread, it can extract the rest of that thread and export it as a text file.
- \[I\]ndex: Given the id of the last tweet in an index thread (ie: a thread composed of qrts of other threads), it can extract each qrted thread and export them as text files (with names reflecting any caption present in the index).

## Flaws:
- No provisions are made to handle branching threads and I haven't tested how it reacts to them. Some tweets may be lost.
- In \[S\]earch and \[H\]unt, Output text files are named based on the ID and time of the final tweet in each thread, instead of the initial one.
- \[I\]ndex is not fully tested and may break in some situations.
- While the script attempts to strip numbering from tweets (eg trailing "y/" or "y/x"), this is imperfect.