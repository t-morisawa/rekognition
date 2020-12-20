import responder
import reprlib
import aioboto3
import asyncio
import twitter
import aiohttp
from typing import List
from face_detector import FaceDetector


api = responder.API(cors=True, cors_params={
    'allow_origins': ['*'],
    'allow_methods': ['*'],
    'allow_headers': ['*'],
})

@dataclass
class FileResponse:
    pass


@dataclass
class TwitterResponse:
    pass


@api.route("/")
async def file_api(req, resp):

    data = await req.media(format='files')

    # データ生成
    file_images_list = []
    for key, value in data.items():
        file_image = FileImage(key, value['content'], {})
        file_images_list.append(file_image)
    file_images = FileImages(file_images_list)

    # 顔認識    
    print(reprlib.repr(data))
    detectfaces = FaceDetector()
    await detectfaces.detect(file_images)

    # 結果を格納
    # TODO  適当な配列ではなく、dataclassを定義する
    results = []
    for image in file_images.images:
        results.append({'result': image.result})

    resp.media = results


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
