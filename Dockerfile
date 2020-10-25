FROM python:3

WORKDIR app

COPY src/requirements.txt /app/src/requirements.txt

RUN pip install -r src/requirements.txt

CMD python