import twitter

# initialize api instance
twitter_api = twitter.Api(consumer_key='JvaUYSYyckryhmmCNQLp4DuK6',
                        consumer_secret='3p07FNUAKUJMpg9ANpCgEBrVAqw8H4dcAVACjWO1FZEDBsNsg9',
                        access_token_key='1276677741799186432-bxjvVd7dX4wk4P7cegysfHi1fYFbYu',
                        access_token_secret='XAAKBrOQMw0CavFPTeWptsv8un1xrVNhVgDc1dBKCBqWB')

# test authentication
print(twitter_api.VerifyCredentials())

# ------------------------------------------------------------------------

def buildTestSet(search_keyword):
    try:
        tweets_fetched = twitter_api.GetSearch(search_keyword, count=100)
        
        print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " + search_keyword)

        return [{"text":status.text, "label":None} for status in tweets_fetched]
    except:
        print("Unfortunately, something went wrong..")
        return None
    
# ------------------------------------------------------------------------

search_term = raw_input("Enter a search keyword: ")
testDataSet = buildTestSet(search_term)

print(testDataSet[0:4])

# ------------------------------------------------------------------------

def buildTrainingSet(corpusFile, tweetDataFile):
    import csv
    import time 

    corpus=[]
    
    with open(corpusFile,'r') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            corpus.append({"tweet_id":row[2], "label":row[1], "topic":row[0]})
    
    rate_limit=180
    sleep_time=900/180
    
    trainingDataSet=[]

    for i in range (0,20):
        try:
            status = twitter_api.GetStatus(corpus[i]["tweet_id"])
            print("Tweet fetched" + status.text)
            tweet["text"] = status.text
            trainingDataSet.append(tweet)
            time.sleep(sleep_time)
        except: 
            continue
    # Now we write them to the empty CSV file
    with open('tweetDataFile.csv','wb') as csvfile:
        linewriter=csv.writer(csvfile,delimiter=',',quotechar="\"")
        for tweet in trainingDataSet:
            try:
                linewriter.writerow([tweet["tweet_id"],tweet["text"],tweet["label"],tweet["topic"]])
            except Exception as e:
                print(e)
    return trainingDataSet

# ------------------------------------------------------------------------

corpusFile = "twitter-sentiment-training/corpus.csv"
tweetDataFile = "twitter-sentiment-training/tweetDataFile.csv"

trainingData = buildTrainingSet(corpusFile, tweetDataFile)

# ------------------------------------------------------------------------