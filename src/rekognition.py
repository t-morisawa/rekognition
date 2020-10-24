import boto3
import sys
import json

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


def detect_faces(image_bytes):
    response = client.detect_faces(
        Image={
            'Bytes': image_bytes,
        },
        Attributes=[
            'ALL',
        ]
    )
    return response


if __name__ == '__main__':
    args = sys.argv
    filename = args[1]
    print(filename)
    result = detect_faces(get_image_from_file(filename))
    print(result)
    print(len(result['FaceDetails']))
