import tweepy

consumer_key = '***'
consumer_secret = '***'
access_token = '***'
access_token_secret = '***'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class GetTweetImage:

    def __init__(self):
        self.result = []

    def get_imge_url(self, accountName):
        #key_account = input('Enter account name:')
        #count_no = int(input('Set search count:'))
        #search_results = tweepy.Cursor(api.user_timeline, screen_name=key_account).items(count_no)
        search_results = tweepy.Cursor(api.user_timeline, screen_name=accountName).items(5)

        for result in search_results:
            img_url = result.extended_entities['media'][0]['media_url']
            print(str(img_url))

        self.result.append(img_url)

    return self.result