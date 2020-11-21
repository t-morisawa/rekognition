import tweepy
import requests

consumer_key = 'GmcKASG6OvocBPWGoGvvXqn1g'
consumer_secret = '0OvnaVOWIwLgLujpM6AYzVY7hKWFJzILuvfYwCGmJiSLRauTur'
access_token = '1128263296006512642-j9xkJezcoHEjxhbLm3PlHt9TrVOib4'
access_token_secret = 'mtm7zJBq7ysW5FmgkT9DcXc95PPCBTcaZTEFfabePiXBF'

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

    def __init__(self):
        self.img_url = []

    def get_imge_url(self, accountName):
        #key_account = input('Enter account name:')
        #count_no = int(input('Set search count:'))
        #search_results = tweepy.Cursor(api.user_timeline, screen_name=key_account).items(count_no)
        search_results = tweepy.Cursor(api.user_timeline, screen_name=accountName, include_rts=False).items(100)

        for result in search_results:
            if hasattr(result, 'extended_entities'):
                self.img_url.append(result.extended_entities['media'][0]['media_url'])
                print(str(self.img_url))
        
        #画像の数だけ処理する必要あり
        #response = requests.get(self.img_url[0])

        #print(response.content)
        #return response.content
        return self.img_url

if __name__ == '__main__':
    g = GetTweetImage()
    g.get_imge_url("pikarox1")