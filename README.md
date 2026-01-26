# LINCC Frameworks Pre-Commit Hooks for Python Project Template

[![Template](https://img.shields.io/badge/Template-LINCC%20Frameworks%20Python%20Project%20Template-brightgreen)](https://lincc-ppt.readthedocs.io/en/latest/)

## Check template version

### Motivation

The [LINCC Frameworks Python Project Template](https://lincc-ppt.readthedocs.io/en/latest/)
is a reference implementation for our team's 
python best practices. These best practices change over time (or we adapt to changes in 
other systems), and the PPT copier template is updated and released.

This pre-commit check determines if your current PPT copier template is up-to-date
and provides a warning if it's not. You can still continue with your commit if the 
template is stale, but we recommend running the update process.

### Configuration

Add the following to your `.pre-commit-config.yaml` file to check for newer versions 
of the template:

```
repos:

...

  - repo: https://github.com/lincc-frameworks/pre-commit-hooks
    rev: v0.1.2
    hooks:
      - id: check-lincc-frameworks-template-version
        name: Check template version
        description: Compare current template version against latest
        verbose: true

...
```

### Execution

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

A new version of your project template is available!
Your version (1.3.0) is older than the latest (1.3.1)
Run the following command to update your template: copier
For more information see the documentation: https://lincc-ppt.readthedocs.io/en/latest/source/update_project.html
```


## Check pre-executed notebooks

### Motivation

Often, tutorial notebooks require large datasets, access to third party APIs, large CPU or GPU requirements.

In our projects, we want to include these in rendered readthedocs sites, but do NOT want them to be 
executed as part of the docs workflow.

To ensure that the notebooks are not run by the notebook conversion process, you can add the following metadata block to the notebook:

```
   "nbsphinx": {
    "execute": "never"
   },
```

The `pre-executed-nb-never-execute` hook was built to check all notebooks inside some `pre_executed` directory
for this metadata block. If it is not present, we add the block. We also confirm that the metadata is well-formatted.

### Configuration

Add the following to your `.pre-commit-config.yaml` file to check notebook metadata:

```
repos:

...
  - repo: https://github.com/lincc-frameworks/pre-commit-hooks
    rev: v0.1.2
    hooks:
      - id: pre-executed-nb-never-execute
        name: Check pre-executed notebooks
        files: ^docs/pre_executed/.*\.ipynb$
        verbose: true
        args:
          ["docs/pre_executed/",]
...
```

### Execution

If all notebooks are found to be in good order, expect the following output
in your pre-commit logs:

```
Check pre-executed notebooks.............................................Passed
```

If some notebooks are modified by this hook, the hook will fail, with a message that 
includes the paths to the modified notebooks.
```
Check pre-executed notebooks.............................................Failed
- hook id: pre-executed-nb-never-execute
- exit code: 1
- files were modified by this hook

Modified notebook to set nbsphinx.execute='never': docs/pre_executed/intro.ipynb
```

Further, if notebooks are malformed, the errors will appear in the pre-commit
logs.

```
Check pre-executed notebooks.............................................Failed
- hook id: pre-executed-nb-never-execute
- exit code: 1

Expecting property name enclosed in double quotes: line 85 column 1 (char 2195)
```

## Attribution

This project was automatically generated using the LINCC-Frameworks [python-project-template](https://github.com/lincc-frameworks/python-project-template).

For more information about the project template see the [documentation](https://lincc-ppt.readthedocs.io/en/latest/).
