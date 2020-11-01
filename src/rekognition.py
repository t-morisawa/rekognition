import boto3
import sys
import json
import asyncio

with open("src/aws.json", "r") as f:
    AWS_PROFILES = json.load(f)

client = boto3.client('rekognition',
                      region_name=AWS_PROFILES['AWS_DEFAULT_REGION'],
                      aws_access_key_id=AWS_PROFILES['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=AWS_PROFILES['AWS_SECRET_ACCESS_KEY'],
)

def get_image_from_file(filename):
    with open(filename, "rb") as f:
        image_bytes= f.read()

    return image_bytes

async def gather(args, detectfaces):
    await asyncio.gather(*[detectfaces.detect_faces(x) for x in args])

class DetectFaces:
    def __init__(self):
        self.result = []

    async def detect_faces(self, image_bytes):
        filename = image_bytes
        result = client.detect_faces(
            Image={
                'Bytes': get_image_from_file(image_bytes),
            },
            Attributes=[
                'ALL',
            ]
        )

        self.result.append({"filename":filename, "result":result})

        #print(len(result['FaceDetails']))

    def get_result(self):
        return self.result
    
if __name__ == '__main__':
    args = sys.argv

    args.pop(0)

    detectfaces = DetectFaces()

    asyncio.run(gather(args,detectfaces))

    print(detectfaces.get_result())
