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

Testing runs against GitHub repositories.
You will quickly run into its rate limiting.
This can be avoided by using a Personal Access Token.

Go to <https://github.com/settings/tokens> and create a new token (no additional scopes necessary).
Set it in your shell:

```
export GITHUB_TOKEN=<the generated token>
```

You can then run the tests:

```
pytest
```

Note: testing might fail due to changing upstream repositories.
