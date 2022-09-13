# fog-update-bot

Automation to update `repositories.yaml` of `probe-scraper` with the latest `metrics_index.py` list.

Fetches and parses the `metrics_index.py` from `gecko-dev`, extracts the relevant list of YAML files
and creates a new Pull Request against `probe-scraper` if it contains any changes.

## Environment variables

| Name | Description |
| ---- | ----------- |
| `DEBUG` | If set enables debug logging |
| `DRY_RUN` | If set to `True` will not create a PR |
| `GITHUB_REPOSITORY_OWNER` | The owner of the `probe-scraper` repository |
| `AUTHOR_NAME` | The name name to use for the commit |
| `AUTHOR_EMAIL` | The email to use for the commit |
| `GITHUB_TOKEN` | The personal access token to access the GitHub API\* |

\*: Can be created on <https://github.com/settings/tokens>. No additional scopes necessary.

## Running with Docker

```
$ docker build -t fog-update .
$ docker run -it --rm fog-update
```

## Development

```
$ python3 -m venv env
$ pip install -r requirements.txt
$ pip install pytest
```

## Testing

You can run the tests:

```
pytest
```

## Code of Conduct

This repository is governed by Mozilla's code of conduct and etiquette guidelines.
For more details, please read the
[Mozilla Community Participation Guidelines](https://www.mozilla.org/about/governance/policies/participation/).

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/

See [LICENSE](LICENSE).
