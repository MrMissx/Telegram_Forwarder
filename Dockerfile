FROM python:3.8-alpine

ENV LANG=C.UTF-8

RUN apk update && apk add --no-cache alpine-sdk \ 
                                     python3-dev \
                                     libffi-dev \
                                     openssl-dev \
                        && rm -rf /var/cache/apk/*
COPY ./ /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app/
CMD ["python3 -m forwarder"]
