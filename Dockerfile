FROM python:3-alpine

ENV egs_username="unset"

RUN printf "\
@edge http://dl-cdn.alpinelinux.org./alpine/edge/main\n\
@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing\n\
@community http://dl-cdn.alpinelinux.org/alpine/edge/community\n\
" >> /etc/apk/repositories

RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk && \
    apk add glibc-2.30-r0.apk && \
    apk add glibc-bin-2.30-r0.apk && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && \
    tar -zxf geckodriver-v0.26.0-linux64.tar.gz -C /usr/bin && \
    rm geckodriver-v0.26.0-linux64.tar.gz
    
COPY requirements.txt /

RUN apk update && apk upgrade && \
    apk add --no-cache \
        firefox@testing \
        tzdata \
        bash && \
    python3 -m pip install -r ./requirements.txt && \
    rm -rf \
        /tmp/* \
        /root/.cache \
        /root/packages

COPY egsfreegamesbot.py /

CMD ["python3", "-u", "/egsfreegamesbot.py"]
