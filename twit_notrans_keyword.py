__date__ = "July 22, 2013"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["Justin Jessup"]
__license__ = "GPL"
__version__ = "0.0.4"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Prototype"


"""
- Twitter Stream API v1.1 Real Time Monitoring 
- Follow Target User/s Tweet Stream of Whom they are Following 
- Track Tweets of whom they are following for keywords 
"""


import oauth2
import json
import tweetstream
import time
from itertools import chain
from colors import TerminalController


def get_following_ids(consumer_key, consumer_secret, access_token, access_secret, twitter_user_name):
    """Oauth2 authentication required for Twitter API v1.1"""
    consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
    access_token = oauth2.Token(key=access_token, secret=access_secret)
    client = oauth2.Client(consumer, access_token)
    following = "https://api.twitter.com/1.1/friends/ids.json?cursor=-1&screen_name=" + twitter_user_name + "&count=5000"
    response, data = client.request(following)
    json_object = json.loads(data)
    twitter_id_list = []
    for following_id in json_object['ids']:
        twitter_id_list.append(following_id)
    yield list(chain(twitter_id_list))
  

def findReplaceAll(text, dic):
    """Find elements within string and replace"""
    for key, value in dic.iteritems():
        text = text.replace(key, value)
    return text


def twitterStream(consumer_key, consumer_secret, access_token, access_secret, twitter_user_name, keywords):
    """Watch Twitter RealTime Stream - Follow Twitter ID's Twitter Target User is Following - and Track List of Keywords Within Whom they are following Twitter Stream"""
    for follow_ids in get_following_ids(consumer_key, consumer_secret, access_token, access_secret, twitter_user_name):
        with tweetstream.FilterStream(consumer_key, consumer_secret, access_token, access_secret, follow=follow_ids, track=keywords) as stream:
            for tweet in stream:
                try:
                    if 'web' in tweet['source']:
                        source_platform = tweet['source']
                    else:
                        source_platform = tweet['source'].split('"')[4].split('>')[1].split('<')[0]
                    tweet_time = tweet['created_at']
                    pattern = '%a %b %d %H:%M:%S +0000 %Y'
                    creation_time = int(time.mktime(time.strptime(tweet_time, pattern))) * 1000
                    geo_location = tweet['geo']
                    coordinates = tweet['coordinates']
                    twitter_id = str(tweet['user']['id'])
                    twitter_screen_name = tweet['user']['screen_name']
                    twitter_proper_name = tweet['user']['name']
                    reply_to_id = tweet['in_reply_to_user_id_str']
                    reply_to_screen_name = tweet['in_reply_to_screen_name']
                    source_lang = tweet['user']['lang']
                    tweet_en = tweet['text']
                    keys = ["Ctime", "Geo", "Coordinates", "Platform", "TwitterID", "ScreenName", "ProperName",
                        "ReplyToID", "ReplyToScreenName", "SourceLang", "Tweet"]
                    values = [creation_time, geo_location, coordinates, source_platform, twitter_id, twitter_screen_name,
                          twitter_proper_name, reply_to_id, reply_to_screen_name,
                          source_lang, tweet_en]
                    twit_dict = dict(zip(keys, values))
                    yield twit_dict
                except KeyError:
                    pass
                       

def main():
    """Color Highligh Keywords Printed to STDOUT Within Tweet Messages"""
    consumer_key = 'lMVKTGsY7LMHS0g6Ktxw'
    consumer_secret = 'Khi8QX7bvE2MW6iqHq7pyRrv0eFZUnljwunmugjk'
    access_token = '400841479-CckMUnIFUzOpd0PhymOslaoNP9gJjxiWNxdGRFzo'
    access_secret = 'LhiAFLuZrwH3VjXiEzhL7fg8z69DtZglLy62UOEk'
    twitter_user_name = "AnonymousIRC"
    keywords = [" FBI ", " NSA ", " CIA "]
    for element in twitterStream(consumer_key, consumer_secret, access_token, access_secret, twitter_user_name, keywords):
        for item in keywords:
            if item.lower() in element['Tweet'].lower():
                highlight = {item: TerminalController().CYAN + item.lower() + TerminalController().NORMAL}
                print(findReplaceAll(element['Tweet'], highlight))


if __name__ == '__main__':
    main()
