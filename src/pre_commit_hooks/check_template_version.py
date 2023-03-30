"""This module is meant to be used in a pre-commit check for projects created 
from a Copier template.
It compares the local template version against the remote template version. 
It prints a message to the screen if the user should update their template.
It will always pass the pre-commit check, i.e. it will always return 0.

The central tenet here is that we don't want to block the users work. We only 
want to make them aware that they could update their template version.
Thus if there are any exceptions raise, we should just treat it as though the 
test passed and return 0.
"""
from __future__ import annotations

import argparse
import os
from typing import Sequence

import git
import yaml
from packaging.version import InvalidVersion, Version, parse


class FriendlyException(Exception):
    "Something went wrong, but we don't want to block committing."
    pass


def _does_file_exist(copier_answer_file: str) -> bool:
    return os.path.isfile(copier_answer_file)


def _get_template_version(copier_config: dict) -> Version:
    try:
        return parse(copier_config.get("_commit", None))
    except (TypeError, InvalidVersion) as exc:
        raise FriendlyException("Cannot parse version string") from exc


def _get_template_path(copier_config: dict) -> str:
    try:
        template_url = copier_config.get("_src_path", None)
        return template_url.replace("gh://", "https://github.com/")
    except AttributeError as exc:
        raise FriendlyException("Cannot return _src_path for copier answers") from exc


def _get_latest_remote_version(template_url: str) -> Version:
    try:
        remote_tags = _retrieve_git_remote_tags(template_url)
        return _parse_git_blob(remote_tags)
    except (Exception, FriendlyException) as exc:
        raise FriendlyException("Failed to get latest version of remote template") from exc


def _retrieve_git_remote_tags(template_url: str) -> str:
    try:
        g = git.cmd.Git()
        return g.ls_remote(template_url, sort="-v:refname", tags=True)
    except Exception as exc:
        raise FriendlyException("Failed to get remote tags") from exc


def _parse_git_blob(git_ls_remote_blob: str) -> Version:
    try:
        return parse(git_ls_remote_blob.split("\n")[0].split("/")[-1])
    except (AttributeError, InvalidVersion, IndexError) as exc:
        raise FriendlyException("Parsing the results of git ls-remote failed") from exc


def _compare_versions(local_template_version: Version, latest_remote_version: Version) -> None:
    try:
        if local_template_version < latest_remote_version:
            print("A new version of your project template is available!")
            print(
                f"Your version ({local_template_version}) is older than the latest ({latest_remote_version})"
            )
            print("Run the following command to update your template: \033[91mcopier\033[0m")
            print(
                "For more information see the documentation: https://lincc-ppt.readthedocs.io/en/latest/source/update_project.html"
            )
        else:
            return 0
    except Exception as exc:
        raise FriendlyException("Failed to compare verisons")


def check_version(copier_answers_file: str) -> int:
    """The main method"""

    # If we can't find the file, we'll just return 0 and move on
    if not _does_file_exist(copier_answers_file):
        return 0

    # If we fail to load the copier answers file, return 0 and move on
    with open(copier_answers_file, "r", encoding="UTF-8") as stream:
        try:
            copier_config = yaml.safe_load(stream)
        except yaml.YAMLError:
            return 0

    try:
        local_copier_version = _get_template_version(copier_config)
    except FriendlyException:
        return 0

    try:
        template_url = _get_template_path(copier_config)
    except FriendlyException:
        return 0

    try:
        latest_remote_version = _get_latest_remote_version(template_url)
    except FriendlyException:
        return 0

    try:
        _compare_versions(local_copier_version, latest_remote_version)
    except FriendlyException:
        return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Parse input arguments and return results of `check_version`"""

    parser = argparse.ArgumentParser()

    # --copier-answers-file will default to .copier-answers.yml, but allows for
    # passing different values in order to support projects that are composed of
    # multiple templates.
    parser.add_argument(
        "--copier-answers-file",
        default=".copier-answers.yml",
        help="The name of the copier answers file. Typically .copier-answers.yml",
    )

    args = parser.parse_args(argv)

    try:
        return check_version(args.copier_answers_file)
    except Exception:
        return 0


if __name__ == "__main__":
    SystemExit(main())
