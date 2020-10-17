import boto3
import base64
import sys

client = boto3.client('rekognition')


def encode_faces(filename):
    with open(filename, "rb") as f:
        bImgBase64 = base64.b64encode(f.read())
    return bImgBase64


def detect_faces(images_b64):
    response = client.detect_faces(
        Image={
            'Bytes': image_b64,
        },
        Attributes=[
            'ALL',
        ]
    )
    return response


if __name__ == '__main__':
    args = sys.argv
    filename = args[0]
    print(filename)
    result = detect_faces(encode_faces(filename))
    print(result)
