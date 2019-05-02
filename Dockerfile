FROM python:3.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /usr/src/app

ENV FLASK_APP app.py

EXPOSE 80

CMD ["flask", "app", "--host=0.0.0.0", "--port=80"]