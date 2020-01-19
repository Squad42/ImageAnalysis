FROM python:3.6.8-alpine

LABEL Squad42 project: image for ImageAnalysis microservice

COPY imageAnalysis/ /imageAnalysis
COPY requirements.txt /imageAnalysis/
WORKDIR /imageAnalysis/


RUN pip3 install --upgrade pip

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk del build-deps

RUN pip3 install -r requirements.txt

EXPOSE 5004

ENV FLASK_APP=server.py
CMD ["python3","-m","flask","run", "--host", "0.0.0.0", "--port", "5004"]
