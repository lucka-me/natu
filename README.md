# Natu
[![License](https://img.shields.io/github/license/lucka-me/natu)](./LICENSE "License")

Yet another fork & enhancement of [`youtube-dl-server`](https://github.com/manbearwiz/youtube-dl-server).

Web UI and REST API built with [`bottle`](https://github.com/bottlepy/bottle) for [`youtube-dl`](https://github.com/rg3/youtube-dl).

## Usage

### Launch the Server
#### Parameters

| Parameter | Description
| :-------- | :----------
| `-e YDL_OUTPUT_TEMPLATE` | Output format, `./downloads/%(title)s [%(id)s].%(ext)s` for default
| `-e NATU_HOST` | Host address, `0.0.0.0` for default
| `-e NATU_PORT` | Host port, `80` for default
| `-e NATU_ROOT` | Root of the server, `/` for default
| `-e NATU_TITLE` | Title displayed on the web UI, `Natu` for default

#### Examples

- Run a container from CLI:
    ```shell
    docker run -d                   \
      --name natu                   \
      --restart always              \
      -e NATU_ROOT=/natu/           \
      -e NATU_TITLE=My Natu         \
      -v ./downloads:/opt/downloads \
      -p 8080:80                    \
      luckame/natu
    ```

- Run a container with `docker-compose.yml`:
    ```yml
    version: '3'

    services:
      natu:
        image: luckame/natu
        container_name: natu
        restart: always
        environment:
          - NATU_ROOT=/natu/
          - NATU_TITLE=My Natu
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

Natu is modified from [`youtube-dl-server`](https://github.com/manbearwiz/youtube-dl-server).

The Web UI is hosted by [`bottle`](https://github.com/bottlepy/bottle).

Videos are downloaded with [`youtube-dl`](https://github.com/rg3/youtube-dl).