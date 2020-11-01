# import boto3
import sys
import json
import asyncio
import aioboto3
import time

with open("src/aws.json", "r") as f:
    AWS_PROFILES = json.load(f)

def get_image_from_file(filename):
    with open(filename, "rb") as f:
        image_bytes= f.read()

    return image_bytes

async def gather(args, detectfaces):
    await asyncio.gather(*[detectfaces.detect_faces(x) for x in args])

class DetectFaces:
    def __init__(self):
        self.result = []

    async def detect_faces(self, image_bytes, client):
        filename = image_bytes
        result = await client.detect_faces(
            Image={
                'Bytes': get_image_from_file(image_bytes),
            },
            Attributes=[
                'ALL',
            ]
        )

        self.result.append({"filename":filename, "result":result})
        print("finished: " + filename)
        #print(len(result['FaceDetails']))

    def get_result(self):
        return self.result

async def main(args, detectfaces):
    async with aioboto3.client('rekognition',
                      region_name=AWS_PROFILES['AWS_DEFAULT_REGION'],
                      aws_access_key_id=AWS_PROFILES['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=AWS_PROFILES['AWS_SECRET_ACCESS_KEY'],
    ) as client:
        await asyncio.gather(*[detectfaces.detect_faces(x, client) for x in args])

if __name__ == '__main__':
    args = sys.argv

    args.pop(0)

    detectfaces = DetectFaces()

    start = time.time()
    asyncio.run(main(args,detectfaces))
    elapsed = time.time() - start

    print(f"{elapsed:.3f}s")  # 秒
    print(f"{elapsed * 1000:.0f}ms")  # ミリ秒
    print(f"{elapsed * 1000000:.0f}μs")  # ナノ秒

    print(detectfaces.get_result())
