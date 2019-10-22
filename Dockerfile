FROM python:3.6-alpine3.8 as BUILD

RUN apk add --update \
    && apk add --no-cache build-base curl-dev linux-headers bash git musl-dev\
    && apk add --no-cache libressl-dev libffi-dev autoconf\
    && rm -rf /var/cache/apk/*

COPY requirements.txt /root/legastress/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /root/legastress/requirements.txt

FROM python:3.6-alpine3.8

LABEL maintainer "NeIC System Developers"
LABEL org.label-schema.schema-version="1.0"

RUN apk add --update \
    && apk add --no-cache libzmq\
    && rm -rf /var/cache/apk/*

RUN addgroup -g 1000 lega && \
    adduser -D -u 1000 -G lega lega

RUN mkdir /results && \
    chmod 777 /results

VOLUME /results

COPY --from=BUILD /usr/local/lib/python3.6/ usr/local/lib/python3.6/

COPY --from=BUILD /usr/local/bin/locust /usr/local/bin/

COPY locustfiles /locustfiles

ADD entrypoint.sh .

VOLUME /conf

ENTRYPOINT [ "/bin/sh", "entrypoint.sh" ]
