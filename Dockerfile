FROM python:3.7-alpine

ADD . /var/www/anagrams-search-service

WORKDIR /var/www/anagrams-search-service

RUN pip install -r requirements.txt

CMD python app.py