#
# youtube-dl-server Dockerfile
#
# https://github.com/lucka-me/natu
#

FROM python:alpine

RUN apk add --no-cache \
  ffmpeg \
  tzdata

RUN mkdir -p /opt
WORKDIR /opt

COPY requirements.txt /opt/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt

EXPOSE 80

CMD [ "python", "-u", "./main.py" ]