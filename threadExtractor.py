import json, re
import string
from urllib.request import urlopen

f = open('tweet.json', encoding="utf8", errors ="replace")
data = json.load(f)

# Regex to trim "x/y" numbering during export.
trimmer = re.compile("([0-9]+|end)\/\n{0,1}")
# Regex to find t.co shortened links
tco_hunter = re.compile("(https:\/\/t.co\/.{10})")
# Regex to extract tweet ids from links
tweet_id_finder = re.compile("https:\/\/twitter.com\/[^\/]+\/status\/(\d+)")

library = {}

who_are_you = ""

# Move tweets into dictionary
for tweet in data:
    library[tweet["tweet"]["id"]] = tweet["tweet"]

# Compiles and trims threads by the ID of their final tweet
def compileThread(target_tweet: str):
    extracts = [library[target_tweet]]

    while target_tweet := extracts[-1].get("in_reply_to_status_id"):
        if library.get(target_tweet):
            extracts.append(library.get(target_tweet))
        else:
            break

    compilation = ("\n\n".join((tweet["full_text"] for tweet in reversed(extracts))))

    return(re.sub(trimmer, '', compilation))

# like compileThread(), but reads from a completed `chains` dictionary
# (like the one that threadHuntCore() returns)
def extractThread(target_tweet: str, chains: dict, reverse=True):
    if target_tweet in chains:
        thread = chains[target_tweet]
    else:
        raise Exception("Couldn't find a thread with that identifier!")

    compilation = "\n\n".join(library.get(tweet)["full_text"] for tweet in thread)

    return(re.sub(trimmer, '', compilation))

# Prints a thread by the ID of its final tweet
def threadSearch():
    print("Please enter the numerical id of the last tweet in the thread.")
    while target_tweet := input("> "):
        print(compileThread(target_tweet))

# This horrible beast of a function
# Attempts to find chains of tweets and ...
# Gods I can't even explain this
# It sucks.
def threadHuntCore():
    chains = {}
    relations = {}

    # Index replies by the ID of the tweet they're reply ing to.
    # Yes, this breaks on branching threads.
    for key in library:
        tweet = library[key]
        try:
            if tweet.get("in_reply_to_screen_name").lower() == who_are_you:
                relations[tweet.get("in_reply_to_status_id")] = tweet["id"]
        except AttributeError:
            pass

    for key in relations:
        lock = relations[key]
        chain = [key, lock]
        while id := relations.get(chain[-1]):
            chain.append(id)

        if not chains.get(chain[-1]):
            chains[chain[-1]] = chain
        elif len(chains.get(chain[-1])) < len(chain):
            chains[chain[-1]] = chain
    
    return chains

def threadHunt():
    chains = threadHuntCore()
    
    print("Found {} threads.".format(len(chains)))

    if input("Output files? [Y/N] ").lower() == "y":
        for key in chains:
            with open(key + " " + library[key]["created_at"].replace(":","-")+".txt", "w",  encoding="utf8", errors ="replace") as file:
                file.write(extractThread(key,chains))
        print("Threads exported!")
    else:
        print("Exiting ...")

def indexHunt():
    print("Please enter the numerical id of the first or last tweet in your index thread.")
    thread_marker = input("> ")

    reverse_chains = threadHuntCore()
    chains = {}
    
    for key in reverse_chains:
        chains[reverse_chains.get(key)[0]] = reverse_chains.get(key)
    
    index_thread = []
    if thread_marker in chains:
        for tweet in chains[thread_marker]:
            index_thread.append(library.get(tweet)["full_text"])
    elif thread_marker in reverse_chains:
        for tweet in reverse_chains[thread_marker]:
            index_thread.append(library.get(tweet)["full_text"])
    else:
        print("No thread found with that head or tail, please double-check the id.")

    index_threads = {}

    print("If I proceed, I will automatically output indexed threads as I find them.")
    if input("Is this okay? [Y/N] ").lower() == "y":
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        for tweet in index_thread:
            print(tweet)
            if re.search(tco_hunter, tweet):
                url = re.search(tco_hunter, tweet).group(0)
                url = urlopen(url).url
                print(url)
                
                if re.search(tweet_id_finder, url):
                    id = re.search(tweet_id_finder, url).group(1)
                    
                    filename = key + " " + tweet + ".txt"
                    filename = re.sub(tco_hunter, '', filename)
                    filename = filename.replace("///", "-")

                    filename = ''.join(c for c in filename if c in valid_chars)        
                    if id in chains:
                        index_threads[id] = chains[id]
                        with open(filename, "w",  encoding="utf8", errors ="replace") as file:
                            file.write(extractThread(id,chains))
                    elif id in library:
                        with open(filename, "w",  encoding="utf8", errors ="replace") as file:
                            file.write(library.get(id)["full_text"])
                    else:
                        print("Failed to find tweet '{}' in tweets.json.\
                            This could be because your index thread links to other accounts' tweets.".format(id))
    
        print("Found and extracted {} threads. Exiting ...".format(len(index_threads)))
    else:
        print("Exiting ...")

                
        

# Options
who_are_you = input("What is your twitter username? @").lower()

match input("[S]earch, [H]unt, or [I]ndex? ").lower():
    case "s":
        threadSearch()
    case "h":
        threadHunt()
    case "i":
        indexHunt()
    case _:
        print("???")
