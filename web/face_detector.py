import responder
import aioboto3
import asyncio
import twitter
import aiohttp
import json
from dataclasses import dataclass


with open("config.json", "r") as f:
    CONFIG = json.load(f)


@dataclass
class FileImage:
    key: str
    content: bytes
    result: dict


@dataclass
class FileImages:
    images: List[FileImage]


class FaceDetector:
    """
    顔認証クラス

    利用方法
    await FaceDetector().detect(image_files)
    """    
    def __init__(self):
        self.result = {}

    async def __single_twitter(self, image_num, filename, imgae_binary, client):
        result = await client.detect_faces(
            Image={
                'Bytes': imgae_binary,
            },
            Attributes=[
                'ALL',
            ]
        )

        self.result[image_num] = {"filename": filename, "result": result}
        print("finished: " + filename)

    async def __single_file(self, image, client):
        result = await client.detect_faces(
            Image={
                'Bytes': image.content,
            },
            Attributes=[
                'ALL',
            ]
        )

        image.result = result

    async def detect(self, data: FileImages):
        """
        顔認証メソッド

        :param list image_files ファイル名のリスト
        """
        async with aioboto3.client('rekognition',
            region_name=CONFIG['AWS_DEFAULT_REGION'],
            aws_access_key_id=CONFIG['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=CONFIG['AWS_SECRET_ACCESS_KEY'],
        ) as client:
            await asyncio.gather(*[self.__single_file(image, client) for image in data.images])

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
            await asyncio.gather(*[self.__single_twitter(index, twitter_image.url, twitter_image.content, client) for index, twitter_image in enumerate(twitter_images.images)])

        # 顔認識の結果を格納
        # TODO あとで直す
        for index, twitter_image in enumerate(twitter_images.images):
            twitter_image.result = self.result[index]['result']

        # 結果を生成する
        # TODO あとで直す
        self.result = {}
        for index, twitter_image in enumerate(twitter_images.images):
            self.result[index] = {"filename":twitter_image.url, "result":　twitter_image.result}

    def get_result(self):
        return self.result