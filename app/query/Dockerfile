FROM python:3.12-slim

WORKDIR /usr/src/cloudwalk

COPY ./app/alchemy ./app/alchemy
COPY ./app/requirements.txt .

RUN mkdir -p ./app/output 
RUN pip install --no-cache-dir -r requirements.txt


COPY ./app/query ./app/query


CMD ["python", "-m", "app.query.query"]