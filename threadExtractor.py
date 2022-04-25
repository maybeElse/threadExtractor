import json, re

f = open('tweet.json', encoding="utf8", errors ="replace")
data = json.load(f)

# Regex to trim "x/y" numbering during export.
trimmer = re.compile('([0-9]+|end)\/\n{0,1}')

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

# Prints a thread by the ID of its final tweet
def threadSearch():
    while target_tweet := input("> "):
        print(compileThread(target_tweet))

# This horrible beast of a function
# Attempts to find chains of tweets and ...
# Gods I can't even explain this
# It sucks.
def threadHunt():
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
    
    print(len(chains))

    if input("Output files? [Y/N] ").lower == "y":
        for key in chains:
            with open(key + " " + library[key]["created_at"].replace(":","-")+".txt", "w",  encoding="utf8", errors ="replace") as file:
                file.write(compileThread(key))
        print("Threads exported!")
    else:
        print("Exiting ...")

# Options
who_are_you = input("What is your twitter username? @").lower()

match input("[S]earch or [H]unt? ").lower():
    case "s":
        threadSearch()
    case "h":
        threadHunt()
    case _:
        print("???")