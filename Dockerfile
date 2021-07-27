FROM python:3.9


WORKDIR /code

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . /code

EXPOSE 9000

CMD uvicorn main:app --reload --port 9000 --host 0.0.0.0
