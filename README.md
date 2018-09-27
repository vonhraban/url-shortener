## URL Shortener

### Spinning up locally

Make sure the CONFIG_FILE environment variable is set, this is so that
different config files can be used for different environments.

`export CONFIG_FILE=config.yml`

After the app knows which config to use, spin it up:

```
$ docker-compose up -d
$ gunicorn --reload url_shortener.app:app
```

### Requests and responses 

#### Shorten a url

```
$ curl http://127.0.0.1:8000 -XPOST -d '{"url": "http://wwww.google.com"}' -H 'content-type: application/json'
{"key":"GFtcZe4O8z7fvg=="}
```

#### Retrieve the url
```
$ curl -http://127.0.0.1:8000/GFtcZe4O8z7fvg==                    v http://127.0.0.1:8000/GFtcZe4O8z7fvg==
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> GET /GFtcZe4O8z7fvg== HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.54.0
> Accept: */*
>
< HTTP/1.1 301 Moved Permanently
< Server: gunicorn/19.9.0
< Date: Thu, 27 Sep 2018 14:08:44 GMT
< Connection: close
< content-type: application/json
< content-length: 22
<
* Closing connection 0
{"moved":"http://wwww.google.com"}
```

#### Error handling

```
$ curl http://127.0.0.1:8000 -XPOST -d 'gibberish' -H 'content-type: application/json'
{"error":"Invalid JSON provided"}
```

```
$ curl http://127.0.0.1:8000 -XPOST -d '{"key":"value"}' -H 'content-type: application/json'
{"error":"`url` parameter is required"}
```


### Running tests

```
$ python3 -m pytest tests/
```