FROM python:3.12-slim

WORKDIR /usr/src/cloudwalk

COPY ./app ./app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "app.query.query"]