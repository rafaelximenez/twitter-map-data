from engine.services.sentiment_analysis import *
from engine.services.twitter import *

from datetime import datetime
import pandas as pd
import logging
import os

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

os.environ['BUCKET_NAME'] = 'rxmz-bot-bkt'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

tt = Twitter()
gnlp = GNaturalLanguage()

logging.info('Buscando dados no twitter')
data = tt.get_tt_data('gafisa')

df_users  = pd.DataFrame()
df_tweets = pd.DataFrame()

logging.info('Percorrendo tweets')
i = 1
for d in data:    
    logging.info(f'Gerando dados [{str(i).zfill(2)}]')
    score, magnitude = gnlp.sentiment_analysis(d.text)
    df_user = {
        'id': d.user.id, 
        'name': (d.user.name).encode('utf8'), 
        'screen_name': (d.user.screen_name).encode('utf8'),
        'profile_image_url': d.user.profile_image_url,
        }

    df_tweet = {
        'id': d.id, 
        'user_id': d.user.id,
        'text': (d.text).encode('utf8'),
        'retweet_count': d.retweet_count,
        'favorite_count': d.favorite_count,
        'lang': d.lang,
        'created_at': d.created_at,
        'sentiment_score': score,
        'sentiment_magnitude': magnitude
    }

    df_users = df_users.append(df_user, ignore_index = True)
    df_tweets = df_tweets.append(df_tweet, ignore_index = True)

    i += 1

year  = str(datetime.now().year)
month = str(datetime.now().month).zfill(2)

df_users.to_csv(f'gs://{os.environ["BUCKET_NAME"]}/rxmz-twitter/nao-processados/tt_users_{year+month}.csv', sep=";", index=False)
df_tweets.to_csv(f'gs://{os.environ["BUCKET_NAME"]}/rxmz-twitter/nao-processados/tt_tweets_{year+month}.csv', sep=";", index=False)