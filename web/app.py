import responder
import reprlib
import aioboto3
import json
import asyncio
import requests
import twitter

api = responder.API(cors=True, cors_params={
    'allow_origins': ['*'],
    'allow_methods': ['*'],
    'allow_headers': ['*'],
})

with open("aws.json", "r") as f:
    AWS_PROFILES = json.load(f)

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
                        region_name=AWS_PROFILES['AWS_DEFAULT_REGION'],
                        aws_access_key_id=AWS_PROFILES['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=AWS_PROFILES['AWS_SECRET_ACCESS_KEY'],
        ) as client:
            await asyncio.gather(*[self.__single(key, value["filename"], value["content"], client) for key, value in data.items()])

    async def tweet_Image(self, accountName):
        """
        顔認証メソッド

        :param list image_files ファイル名のリスト
        """
        getTwitterImage = twitter.GetTweetImage()
        imageUrl = getTwitterImage.get_imge_url(accountName)

        async with aioboto3.client('rekognition',
                        region_name=AWS_PROFILES['AWS_DEFAULT_REGION'],
                        aws_access_key_id=AWS_PROFILES['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=AWS_PROFILES['AWS_SECRET_ACCESS_KEY'],
        ) as client:
            await asyncio.gather(*[self.__single(url, requests.get(url).content, client) for url in imageUrl])

    def get_result(self):
        return self.result