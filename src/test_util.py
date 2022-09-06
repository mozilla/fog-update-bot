# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/


from fog_update import eval_extract, swap_metrics_files


REPOSITORIES_YAML = """
---
version: "2"
applications:
  - app_name: firefox_desktop
    metrics_files: # When adding here, consider if you should also add to pine.
      - METRICS_FILES
    ping_files:
      - PING_FILES
  - app_name: firefox_desktop_background_update
    metrics_files:
      - OTHER_METRICS_FILES
    ping_files:
      - OTHER_PING_FILES
"""

METRICS_INDEX = """
# -*- Mode: python; indent-tabs-mode: nil; tab-width: 40 -*-
# vim: set filetype=python:
metrics_yamls = [
    "A",
    "B",
    "C",
]

pings_yamls = [
    "D",
    "E",
    "F"
]
"""


def test_eval_metrics_index():
    content = eval_extract(METRICS_INDEX, "metrics_yamls")
    assert content == ["A", "B", "C"]


def test_swap_repositories_yaml():
    metrics_files = eval_extract(METRICS_INDEX, "metrics_yamls")
    output = swap_metrics_files(REPOSITORIES_YAML, "firefox_desktop", metrics_files)

    # New files added.
    assert "- METRICS_FILES" not in output
    assert "- A" in output
    assert "- B" in output
    assert "- C" in output
    # ping files untouched.
    assert "- PING_FILES" in output

    # Other app untouched
    assert "- OTHER_METRICS_FILES" in output
    assert "- OTHER_PING_FILES" in output


def test_swap_repositories_yaml_unchanged():
    metrics_files = ["METRICS_FILES"]
    output = swap_metrics_files(REPOSITORIES_YAML, "firefox_desktop", metrics_files)

    # New files added.
    assert "- METRICS_FILES" in output
    assert "- A" not in output
    # ping files untouched.
    assert "- PING_FILES" in output

    # Other app untouched
    assert "- OTHER_METRICS_FILES" in output
    assert "- OTHER_PING_FILES" in output
