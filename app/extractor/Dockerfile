FROM python:3.12-slim

WORKDIR /usr/src/cloudwalk

COPY ./app/alchemy ./app/alchemy 
COPY ./app/requirements.txt .

RUN mkdir -p ./app/database 
RUN pip install --no-cache-dir -r requirements.txt


COPY ./app/extractor ./app/extractor


CMD ["python", "-m", "app.extractor.extract"]