FROM python:3-alpine

COPY requirements.txt /

RUN \
apk update && apk upgrade && \
apk add --no-cache \
    tzdata \
    bash && \
python3 -m pip install -r ./requirements.txt && \
rm -rf \
    /tmp/* \
    /root/.cache \
    /root/packages

COPY egsfreegamesbot.py /

CMD ["python3 egsfreegamesbot.py"]
