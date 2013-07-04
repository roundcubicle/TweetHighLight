__date__ = "February 15, 2013"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["Justin Jessup"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Prototype"

"""Monitor Twitter Real Time Data Stream via a List of keywords"""


import tweetstream
import time
from colors import TerminalController


def findReplaceAll(text, dic):
    """Find elements within string and replace"""
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


def twitterStream(consumer_key, consumer_secret, access_token, access_secret, keywords):
    """Watch Twitter RealTime Stream for WatchList Elements"""
    with tweetstream.FilterStream(consumer_key, consumer_secret, access_token, access_secret, track=keywords) as stream:
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
    consumer_key = 'lMVKTGsY7LMHS0g6Ktxw'
    consumer_secret = 'Khi8QX7bvE2MW6iqHq7pyRrv0eFZUnljwunmugjk'
    access_token = '400841479-CckMUnIFUzOpd0PhymOslaoNP9gJjxiWNxdGRFzo'
    access_secret = 'LhiAFLuZrwH3VjXiEzhL7fg8z69DtZglLy62UOEk'
    keywords = ["anonymous", "egypt"]
    for element in twitterStream(consumer_key, consumer_secret, access_token, access_secret, keywords):
        for item in keywords:
            highlight = {item: TerminalController().CYAN + item + TerminalController().NORMAL}
            print(findReplaceAll(element['Tweet'].lower(), highlight))


if __name__ == '__main__':
    main()
