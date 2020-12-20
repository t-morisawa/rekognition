import tweepy
import os
import json
from dataclasses import dataclass
from datetime import datetime
from typing import List
from container import TwitterImage, TwitterImages

with open("config.json", "r") as f:
    CONFIG = json.load(f)
    consumer_key = CONFIG['TWITTER_CONSUMER_KEY']
    consumer_secret = CONFIG['TWITTER_CONSUMER_SECRET']
    access_token = CONFIG['TWITTER_ACCESS_TOKEN']
    access_token_secret = CONFIG['TWITTER_ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

"""
key_account = input('Enter account name:')
count_no = int(input('Set search count:'))
search_results = tweepy.Cursor(api.user_timeline, screen_name=key_account).items(count_no)

for result in search_results:
    try:
        img_url = result.extended_entities['media'][0]['media_url']
        print(img_url)
    except:
        pass
"""


class GetTweetImage:

    def get_image_url(self, accountName: str) -> List[str]:
        #key_account = input('Enter account name:')
        #count_no = int(input('Set search count:'))
        #search_results = tweepy.Cursor(api.user_timeline, screen_name=key_account).items(count_no)
        search_results = tweepy.Cursor(api.user_timeline, screen_name=accountName, include_rts=False).items(100)

        twitter_images_list = []
        try:
            for result in search_results:
                if hasattr(result, 'extended_entities'):  # 画像ツイート
                    for photo in result.extended_entities['media']:
                        twitter_image = TwitterImage(photo['media_url'], b'', result.created_at, {})
                        twitter_images_list.append(twitter_image)
        except tweepy.error.TweepError:
            # 画像取得タイムアウト例外
            pass

        twitter_images = TwitterImages(twitter_images_list)
        print(twitter_images)
        return twitter_images

if __name__ == '__main__':
    g = GetTweetImage()
    g.get_image_url("pikarox1")