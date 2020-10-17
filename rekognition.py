import boto3
import sys

client = boto3.client('rekognition')


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
