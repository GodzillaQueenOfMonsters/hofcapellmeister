FROM python:3.12

WORKDIR /hcm

COPY . .

RUN pip install -r requirements.txt
