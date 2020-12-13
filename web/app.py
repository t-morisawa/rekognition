import responder
import reprlib
import aioboto3
import json
import asyncio
import requests
import twitter
import aiohttp


api = responder.API(cors=True, cors_params={
    'allow_origins': ['*'],
    'allow_methods': ['*'],
    'allow_headers': ['*'],
})

with open("config.json", "r") as f:
    CONFIG = json.load(f)

@api.route("/")
async def file_api(req, resp):

    data = await req.media(format='files')

    #f = open('./{}'.format(data['file']['filename']), 'w')
    #f.write(data['file']['content'].decode('utf-8'))
    #f.close()

    print(reprlib.repr(data))

    # resp.media = {'filename': str(data["image"]["filename"])}
    #filename = []
    #for v in data.values():
    #filename.append({'filename': v["filename"]})

    detectfaces = FaceDetector()
    await detectfaces.detect(data)
    print(detectfaces.get_result())

    resp.media = detectfaces.get_result()

    #print(data["image"])
    #resp.text = str(data["image"]["filename"])


@api.route("/twitter/{accountName}")
async def twitter_api(req, resp, *, accountName):
    detectfaces = FaceDetector()
    await detectfaces.tweet_Image(accountName)

    """
    print(reprlib.repr(response))
    detectfaces = FaceDetector()
    await detectfaces.detect(response)
    print(detectfaces.get_result())

    resp.media = detectfaces.get_result()

    #print(data["image"])
    #resp.text = str(data["image"]["filename"])
    """
    resp.media = detectfaces.get_result()


class FaceDetector:
    """
    顔認証クラス

    利用方法
    await FaceDetector().detect(image_files)
    """    
    def __init__(self):
        self.result = {}

    async def __single(self, image_num, filename, imgae_binary, client):
        result = await client.detect_faces(
            Image={
                'Bytes': imgae_binary,
            },
            Attributes=[
                'ALL',
            ]
        )

        
        self.result[image_num] = {"filename":filename, "result":result}
        print("finished: " + filename)
        #print(len(result['FaceDetails']))

    async def detect(self, data):
        """
        顔認証メソッド

        :param list image_files ファイル名のリスト
        """
        async with aioboto3.client('rekognition',
                        region_name=CONFIG['AWS_DEFAULT_REGION'],
                        aws_access_key_id=CONFIG['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=CONFIG['AWS_SECRET_ACCESS_KEY'],
        ) as client:
            await asyncio.gather(*[self.__single(key, value["filename"], value["content"], client) for key, value in data.items()])

    async def tweet_Image(self, accountName):
        """
        顔認証メソッド

        :param list image_files ファイル名のリスト
        """
        # 画像URLの取得
        twitter_images = twitter.GetTweetImage().get_image_url(accountName)

        # 画像の取得
        async def request_image(twitter_image: twitter.TwitterImage, session: aiohttp.ClientSession):
            async with session.get(twitter_image.url) as response:
                twitter_image.content = await response.read()

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[request_image(twitter_image, session) for twitter_image in twitter_images.images])

        # 顔認識
        async with aioboto3.client('rekognition',
                        region_name=CONFIG['AWS_DEFAULT_REGION'],
                        aws_access_key_id=CONFIG['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=CONFIG['AWS_SECRET_ACCESS_KEY'],
        ) as client:
            await asyncio.gather(*[self.__single(twitter_image.url, twitter_image.url, twitter_image.content, client) for twitter_image in twitter_images.images])
        
        # 顔認識の結果を格納
        # TODO あとで直す
        for twitter_image in twitter_images.images:
            twitter_image.result = self.result[twitter_image.url]['result']

        # 並び替えの処理を入れる
        sorted(twitter_images.images, key=lambda image: image.created_at)

        # 結果を生成する
        # TODO あとで直す
        self.result = {}
        for index, twitter_image in enumerate(twitter_images.images):
            self.result[index] = {"filename":twitter_image.url, "result":twitter_image.result}
        
    def get_result(self):
        return self.result