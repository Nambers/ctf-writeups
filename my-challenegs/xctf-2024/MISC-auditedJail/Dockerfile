FROM python:3.12.4-alpine@sha256:a982997504b8ec596f553d78f4de4b961bbdf5254e0177f6e99bb34f4ef16f95

RUN apk -U --no-cache upgrade && apk add --no-cache socat

COPY ./start.sh /
RUN chmod +x /start.sh

RUN adduser -D ctf
WORKDIR /home/ctf

COPY ./flag /flag
RUN chmod +r /flag
COPY ./jail.py /home/ctf/jail.py

ENTRYPOINT ["/bin/sh","/start.sh"]
