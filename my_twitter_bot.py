import tweepy
import time
# from keys_format import *
CONSUMER_KEY = 'eiH2wHBWTMrSU3Ksgbzwpq0uo'
CONSUMER_SECRET = '1KzmR1hynDGtYdLpyTajuygBoHCb0q5V0r2TvPERMs6l6OXw5t'
ACCESS_KEY = '896043252704346112-pOHuTnikf6G7wacBnm5op0h7hbeGARL'
ACCESS_SECRET = 'C9yKTObyQIbMGp2KVfw0pBp3nExPjg74cSBGM8Wt6oTuQ'

print("this is my twitter bot")


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(

                        tweet_mode='extended')
    print(f"{mentions}")
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '@ritik' in mention.full_text.lower():
            print('found @ritik!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    '#Hey! ' + mention.user.name, mention.id)

def retweet(api, word = "#awsclpu"):
    tweets = tweepy.Cursor(api.search, q = word, lang = "en",tweet_mode = "extended" ).items(5)
    # print(type(tweets))
    list_tweets = [tweet for tweet in tweets]
    # print(list_tweets)

    for tweet in list_tweets:
        id = tweet.user.id
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']

        # Retweets can be distinguished by a retweeted_status attribute,
        # in case it is an invalid reference, except block will be executed
        print(f"{id}: {username}")
        try:
            api.retweet(id)
            print("retweet succesful")
            api.update_status("Retweeted Succesffuly")
        except tweepy.TweepError:
            print("Already Tweeted!")
        


if __name__ == '__main__':
    retweet(api, "#helloWorld2")
    # reply_to_tweets()
    # time.sleep(15)