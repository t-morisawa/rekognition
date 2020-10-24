FROM python:3

COPY src/requirements.txt /src/requirements.txt

RUN pip install -r src/requirements.txt

COPY src /src
COPY images /images

ENTRYPOINT ["python", "src/rekognition.py"]
