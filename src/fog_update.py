#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

from github import Github, GithubException, InputGitAuthor, enable_console_debug_logging
import datetime
import io
import os
import requests
import sys

DEFAULT_ORGANIZATION = "badboy"
DEFAULT_AUTHOR_NAME = "data-updater"
DEFAULT_AUTHOR_EMAIL = "jrediger@mozilla.com"
USAGE = "usage: fog-update"


def ts():
    return str(datetime.datetime.now())


def eval_extract(code, key):
    """
    Eval `code` and extract the variable named by `key`.

    `code` should be valid Python code.
    No builtins are provided.
    """
    globals = {"__builtins__": {}}
    exec(code, globals)
    return globals[key]


def swap_metrics_files(content, app, metrics_files):
    """
    Replace the list of `metrics_files` in `content` with `metrics_files`.
    Returns the changed content.

    All other content is left untouched.
    YAML syntax is assumed.
    File entries are correctly indented.
    """
    output = io.StringIO()
    state = None
    app = f"- app_name: {app}"
    indent = 0

    for line in content.split("\n"):
        if state is None and line.strip() == app:
            state = "app"
        elif state == "app" and "metrics_files" in line:
            state = "files"
        elif state == "files":
            if line.strip().startswith("-"):
                ws, _ = line.split("-")
                indent = len(ws)
                continue
            else:
                for file in metrics_files:
                    print(" " * indent, file=output, end="")
                    print(f"- {file}\n", file=output, end="")
                state = None

        print(line, file=output)

    return output.getvalue()


def get_latest_metrics_index():
    url = "https://raw.githubusercontent.com/mozilla/gecko-dev/master/toolkit/components/glean/metrics_index.py"  # noqa
    r = requests.get(url)
    r.raise_for_status()
    return r.text


def _update_repositories_yaml(repo, branch, author, app, metrics_yamls):
    contents = repo.get_contents("repositories.yaml", ref=branch)
    content = contents.decoded_content.decode("utf-8")

    new_content = swap_metrics_files(content, app, metrics_yamls)
    if content == new_content:
        raise Exception(
            "Update to repositories.yaml resulted in no changes: maybe the file was already up to date?"  # noqa
        )

    repo.update_file(
        contents.path,
        "Update repositories.yaml with new FOG metrics_yamls list",
        new_content,
        contents.sha,
        branch=branch,
        author=author,
    )


def main(argv, repo, author, debug=False, dry_run=False):
    if len(argv) < 1:
        print(USAGE)
        sys.exit(1)

    release_branch_name = "main"

    if dry_run:
        print(f"{ts()} Dry-run so not continuing.")
        return

    short_version = "main"

    # Create a non unique PR branch name for work on this ac release branch.
    pr_branch_name = f"fog-update/update-metrics-index-{short_version}"

    try:
        pr_branch = repo.get_branch(pr_branch_name)
        if pr_branch:
            print(f"{ts()} The PR branch {pr_branch_name} already exists. Exiting.")
            return
    except GithubException:
        # TODO Only ignore a 404 here, fail on others
        pass

    release_branch = repo.get_branch(release_branch_name)
    print(f"{ts()} Last commit on {release_branch_name} is {release_branch.commit.sha}")

    print(f"{ts()} Creating branch {pr_branch_name} on {release_branch.commit.sha}")
    repo.create_git_ref(
        ref=f"refs/heads/{pr_branch_name}", sha=release_branch.commit.sha
    )
    print(f"{ts()} Created branch {pr_branch_name} on {release_branch.commit.sha}")

    metrics_index = get_latest_metrics_index()
    metrics_yamls = sorted(eval_extract(metrics_index, "metrics_yamls"))

    print(f"{ts()} Updating repositories.yaml")
    _update_repositories_yaml(
        repo, pr_branch_name, author, "firefox_desktop", metrics_yamls
    )

    print(f"{ts()} Creating pull request")
    pr = repo.create_pull(
        title=f"Update to latest metrics_index list on {release_branch_name}",
        body="This (automated) patch updates the list from metrics_index.py",
        head=pr_branch_name,
        base=release_branch_name,
    )
    print(f"{ts()} Pull request at {pr.html_url}")


if __name__ == "__main__":

    debug = os.getenv("DEBUG") is not None
    if debug:
        enable_console_debug_logging()

    github_access_token = os.getenv("GITHUB_TOKEN")
    if not github_access_token:
        print("No GITHUB_TOKEN set. Exiting.")
        sys.exit(1)

    github = Github(github_access_token)
    if github.get_user() is None:
        print("Could not get authenticated user. Exiting.")
        sys.exit(1)

    dry_run = os.getenv("DRY_RUN") == "True"

    organization = os.getenv("GITHUB_REPOSITORY_OWNER") or DEFAULT_ORGANIZATION

    repo = github.get_repo(f"{organization}/probe-scraper")

    author_name = os.getenv("AUTHOR_NAME") or DEFAULT_AUTHOR_NAME
    author_email = os.getenv("AUTHOR_EMAIL") or DEFAULT_AUTHOR_EMAIL
    author = InputGitAuthor(author_name, author_email)

    print(
        f"{ts()} This is fog-update working on https://github.com/{organization} as {author_email} / {author_name}"  # noqa
    )

    main(sys.argv, repo, author, debug, dry_run)