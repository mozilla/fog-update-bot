# fog-update
__Jan-Erik Rediger, September 2022__

Automation to update `repositories.yaml` of `probe-scraper` with the latest `metrics_index.py` list.

### Running with Docker

```
$ docker build -t fog-update .
$ docker run -it --rm fog-update
```

### Development

```
$ python3 -m venv env
$ pip install -r requirements.txt
$ pip install pytest
```

### Testing

You can run the tests:

```
pytest
```
