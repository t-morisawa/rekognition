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
async def hello_world(req, resp):

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
async def hell_world(req, resp, *, accountName):
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
        getTwitterImage = twitter.GetTweetImage()
        imageUrl = getTwitterImage.get_imge_url(accountName)

        # URLの配列 => URLとバイナリの辞書の配列
        images = []
        async def request(url, session):
            async with session.get(url) as response:
                content = await response.read()
                images.append({'url': url, 'content': content})

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[request(url, session) for url in imageUrl])

        async with aioboto3.client('rekognition',
                        region_name=CONFIG['AWS_DEFAULT_REGION'],
                        aws_access_key_id=CONFIG['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=CONFIG['AWS_SECRET_ACCESS_KEY'],
        ) as client:
            await asyncio.gather(*[self.__single(image['url'], image['url'], image['content'], client) for image in images])

    def get_result(self):
        return self.result