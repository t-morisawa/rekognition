FROM python:3

COPY src /src
COPY images /images

RUN pip install -r src/requirements.txt

ENTRYPOINT ["python", "src/rekognition.py"]
