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

    async def detect_faces_from_mulptiple(self, image_files):
        async with aioboto3.client('rekognition',
                        region_name=AWS_PROFILES['AWS_DEFAULT_REGION'],
                        aws_access_key_id=AWS_PROFILES['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=AWS_PROFILES['AWS_SECRET_ACCESS_KEY'],
        ) as client:
            await asyncio.gather(*[self.detect_faces(x, client) for x in image_files])

    def get_result(self):
        return self.result

async def main(image_files):
    detectfaces = DetectFaces()

    start = time.time()
    await detectfaces.detect_faces_from_mulptiple(image_files)
    elapsed = time.time() - start

    print(f"{elapsed * 1000:.0f}ms")  # ミリ秒
    print(detectfaces.get_result())

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:]))
