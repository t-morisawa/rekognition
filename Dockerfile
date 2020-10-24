FROM python:3

COPY src /src

RUN pip install -r src/requirements.txt

ENTRYPOINT ["python", "src/rekognition.py"]
