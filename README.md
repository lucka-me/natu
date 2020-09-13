# Youtube-DL Docker
[![Docker Pulls](https://img.shields.io/docker/pulls/luckame/youtube-dl)](https://hub.docker.com/r/luckame/youtube-dl "Docker Hub") [![Docker Build Status](https://img.shields.io/docker/cloud/build/luckame/youtube-dl)](https://hub.docker.com/r/luckame/youtube-dl/builds "Docker Hub Autobuilds")
[![License](https://img.shields.io/github/license/lucka-me/youtube-dl-docker)](./LICENSE "License")

Yet another fork & enhancement of [`youtube-dl-server`](https://github.com/manbearwiz/youtube-dl-server).

Web UI and REST API built with [`bottle`](https://github.com/bottlepy/bottle) for [`youtube-dl`](https://github.com/rg3/youtube-dl).

## Usage

### Launch the Server
#### Parameters

| Parameter | Description
| :-------- | :----------
| `-e YDL_OUTPUT_TEMPLATE` | Output format, `./downloads/%(title)s [%(id)s].%(ext)s` for default
| `-e WEB_HOST` | Host address, `0.0.0.0` for default
| `-e WEB_PORT` | Host port, `80` for default
| `-e WEB_ROOT` | Root of the server, `/` for default
| `-e WEB_TITLE` | Title displayed on the web UI, `Youtube-DL` for default

#### Examples

- Run a container from CLI:
    ```shell
    docker run -d                   \
      --name youtube-dl             \
      --restart always              \
      -e WEB_ROOT=/youtube-dl/      \
      -e WEB_TITLE=My YTDL          \
      -v ./downloads:/opt/downloads \
      -p 8080:80                    \
      luckame/youtube-dl
    ```

- Run a container with `docker-compose.yml`:
    ```yml
    version: '3'

    services:
      youtube-dl:
        image: luckame/youtube-dl
        container_name: youtube-dl
        restart: always
        environment:
          - WEB_ROOT=/youtube-dl/
          - WEB_TITLE=My YTDL
        volumes:
          - ./downloads:/opt/downloads
        ports:
          - 8080:80
    ```

- Launch with `python@3.6` or later:
    ```shell
    sudo YDL_SERVER_PORT=8123 python3 -u ./main.py
    ```

### Download
#### Web UI

Open `http://{{host}}/`, enter URL, select format and push `Submit`.

#### Terminal

Send a request with `curl`:

```shell
curl -X POST --data-urlencode "url={{url}}" http://{{host}}/query
```

#### Fetch

```javascript
fetch(`http://${host}/query`, {
  method: "POST",
  body: new URLSearchParams({
    url: url,
    format: "bestvideo"
  }),
});
```

#### Bookmarklet

Trigger this bookmarklet to send current URL to the server.

```javascript
javascript:!function(){fetch("http://${host}/query",{body:new URLSearchParams({url:window.location.href,format:"bestvideo"}),method:"POST"})}();
```

## Implementation

This application is modified from [`youtube-dl-server`](https://github.com/manbearwiz/youtube-dl-server).

The Web UI is hosted by [`bottle`](https://github.com/bottlepy/bottle).

Videos are downloaded with [`youtube-dl`](https://github.com/rg3/youtube-dl).