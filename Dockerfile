FROM python:3.11-alpine

LABEL author="Roberto Fioravanti <ing.roberto.fioravanti@gmail.com>"

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /
RUN apk add --update libmagic && \
    pip install -U pip -r /requirements.txt

COPY /src/sendmail.py ./

ENTRYPOINT ["/app/sendmail.py"]
