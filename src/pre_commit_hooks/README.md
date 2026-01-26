# Adding new hooks

This repository can be used for adding new pre-commit hooks, mostly 
that are related to functionality offered by the LINCC Frameworks
Python Project Template.

## Checklist

* Write tests for your new hook
* Implement the hook logic in a new module in this directory
* Make sure that the module contains a `if __name__ == "__main__":` kinda thing
* Include the module in the `./src/__init__.py` file
* Add an entry in the `./.pre-commit-hooks.yaml` file
* Add an entry to `./pyproject.toml` in the `[project.scripts]` section
* Add documentation on the main README to explain 
    * the purpose of the hook
    * how to add the hook to your project
    * what pre-commit success looks like 
    * what pre-commit failures look like