"""This module is meant to be used in a pre-commit check.
It compares the local template version against the remote template version. 
It prints a message to the screen if the user should update their template.
It will always pass the pre-commit check, i.e. it will always return 0.

The central tenet here is that we don't want to block the users work. We only 
want to make them aware that they could update their template version.
Thus if there are any exceptions raise, we should just treat it as though the 
test passed and return 0.
"""
import os
import yaml
import git
from packaging.version import parse, InvalidVersion

def main():
    """The main method"""
    
    copier_answers_file = ".copier-answers.yml"

    # If we can't find the file, we'll just return 0 and move on
    if not os.path.isfile(copier_answers_file):
        return 0

    # If we fail to load the copier answers file, return 0 and move on
    with open(copier_answers_file, "r", encoding="UTF-8") as stream:
        try:
            copier_config = yaml.safe_load(stream)
        except yaml.YAMLError:
            return 0

    # If the semantic version parsing fails, return 0
    try:
        local_copier_version = parse(copier_config.get("_commit", None))
    except InvalidVersion:
        return 0

    # There are bunch of things that could go wrong with git commands, so we'll
    # use a very broad `Exception` class to return 0.
    try:
        g = git.cmd.Git()
        repository = "https://github.com/lincc-frameworks/python-project-template"
        blob = g.ls_remote(repository, sort="-v:refname", tags=True)
    except Exception:
        return 0

    # If the version parsing fails, or the splitting/indexing fails, return 0
    try:
        latest_remote_version = parse(blob.split('\n')[0].split('/')[-1])
    except (InvalidVersion, IndexError):
        return 0

    if local_copier_version < latest_remote_version:
        print(f"Time to update your template version from {local_copier_version} -> {latest_remote_version}")
        print("Run the following command to update your template.")
        print("copier update")

    return 0

if __name__ == '__main__':
    SystemExit(main())
