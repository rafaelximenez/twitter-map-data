from config import (
    TT_CONSUMER_KEY, 
    TT_CONSUMER_SECRET, 
    TT_ACCESS_TOKEN, 
    TT_ACCESS_TOKEN_SECRET
)
from pprint import pprint
import tweepy

class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(TT_CONSUMER_KEY, TT_CONSUMER_SECRET)
    
    def _authetication(self):
        self.auth.set_access_token(TT_ACCESS_TOKEN, TT_ACCESS_TOKEN_SECRET)

        self.api = tweepy.API(self.auth)

    def get_tt_data(self, param):
        self._authetication()
        return tweepy.Cursor(self.api.search, q=param, lang='pt').items(10)