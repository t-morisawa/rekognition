FROM python:3

COPY requirements.txt /
COPY rekognition.py /
COPY sample.jpg /

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "rekognition.py"]
