# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/


from fog_update import eval_extract, swap_file_list


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

first_yamls = ["A", "B"]
second_yamls = ["B", "C"]
metrics_yamls = sorted(list(set(first_yamls + second_yamls)))

pings_yamls = [
    "D",
    "E",
    "F"
]
"""


def test_eval_metrics_index():
    data = eval_extract(METRICS_INDEX)
    assert data["first_yamls"] == ["A", "B"]
    assert data["second_yamls"] == ["B", "C"]
    assert data["metrics_yamls"] == ["A", "B", "C"]


def test_swap_repositories_yaml():
    data = eval_extract(METRICS_INDEX)
    metrics_files = data["metrics_yamls"]
    output = swap_file_list(
        REPOSITORIES_YAML, "firefox_desktop", metrics_files, "metrics"
    )

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
    output = swap_file_list(
        REPOSITORIES_YAML, "firefox_desktop", metrics_files, "metrics"
    )

    # New files added.
    assert "- METRICS_FILES" in output
    assert "- A" not in output
    # ping files untouched.
    assert "- PING_FILES" in output

    # Other app untouched
    assert "- OTHER_METRICS_FILES" in output
    assert "- OTHER_PING_FILES" in output
