# LINCC Frameworks Pre-Commit Hooks for Python Project Template

[![Template](https://img.shields.io/badge/Template-LINCC%20Frameworks%20Python%20Project%20Template-brightgreen)](https://lincc-ppt.readthedocs.io/en/latest/)


Add the following to your `.pre-commit-config.yaml` file to check for newer versions 
of the template:

```
repos:

...

  - repo: https://github.com/lincc-frameworks/pre-commit-hooks
    rev: v0.1
    hooks:
      - id: check-lincc-frameworks-template-version
        name: Check template version
        description: Compare current template version against latest
        verbose: true

...
```

If the template version in the `.copier-answers.yml` file matches the most recent 
version available, you'll see this:

```
Check template version...................................................Passed
- hook id: check-lincc-frameworks-template-version
- duration: 0.59s
```

If your version is behind the most recent, you'll see this:
```
Check template version...................................................Passed
- hook id: check-lincc-frameworks-template-version
- duration: 0.59s

Time to update your template version from 1.3.0 -> 1.3.1
Run the following command to update your template.
copier update
```


## Attribution

This project was automatically generated using the LINCC-Frameworks [python-project-template](https://github.com/lincc-frameworks/python-project-template).

A repository badge was added to show that this project uses the python-project-template, however it's up to
you whether or not you'd like to display it!

For more information about the project template see the For more information about the project template see the [documentation](https://lincc-ppt.readthedocs.io/en/latest/).
