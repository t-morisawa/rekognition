import responder
import reprlib
import aioboto3
import json
import asyncio
import requests
from ..twitter import twitter

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

@api.route("/twitter")
async def hell_world(req, resp):

    getTwitterImage = twitter.GetTwitterImage()
    image_url = getTwitterImage.get_imge_url(await req.text())

    response = requests.get(image_url[0])

    print(reprlib.repr(response))
    detectfaces = FaceDetector()
    await detectfaces.detect(response)
    print(detectfaces.get_result())

    resp.media = detectfaces.get_result()

    #print(data["image"])
    #resp.text = str(data["image"]["filename"])

class FaceDetector:
    """
    顔認証クラス

    利用方法
    await FaceDetector().detect(image_files)
    """    
    def __init__(self):
        self.result = []

    async def __single(self, filename, imgae_binary, client):
        result = await client.detect_faces(
            Image={
                'Bytes': imgae_binary,
            },
            Attributes=[
                'ALL',
            ]
        )

        self.result.append({"filename":filename, "result":result})
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
            await asyncio.gather(*[self.__single(value["filename"], value["content"], client) for value in data.values()])

    def get_result(self):
        return self.result