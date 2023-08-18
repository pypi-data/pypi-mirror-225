# OU Container Builder

Documentation for the OU Container Builder can be found here: https://ou-container-builder.readthedocs.io

![Validation Status](https://github.com/mmh352/ou-container-builder/workflows/Validation/badge.svg) ![Tests](https://github.com/mmh352/ou-container-builder/workflows/Tests/badge.svg) ![Documentation](https://readthedocs.org/projects/ou-container-builder/badge/?version=latest)

# Install and Run

To run the OU Container Builder you need to install the following two requirements:

* [Python 3.8 (or higher)](https://www.python.org/downloads/)
* [Pipx](https://pipxproject.github.io/pipx/)

Then, to install the OU Container Builder run

```
pipx install git+https://github.com/mmh352/ou-container-builder.git
```

To upgrade to the latest version, run:

```
pipx upgrade ou-container-builder
```

You can then run the OU Container Builder using the following command:

```
ou-container-builder
```

## Demo

To build the demo container:

1. Clone the repository
2. Change into the ```demo``` directory
3. Run

   ```
   ou-container-builder
   ```

The resulting container listens for connections on port 8888 and it is recommended that you mount the
```/home/ou-user``` directory as a volume.

## Development

To work on the OU Container Builder you need to install an additional dependency:

* [Poetry](https://python-poetry.org/)

Then use

```
poetry install
```

to install all Python dependencies in a project-specific virtualenv. Then start a shell that runs commands
within that virtualenv:

```
poetry shell
```

You can now run

```
ou-container-builder
```

to run your development version of the code.

### Validation

To automatically check that any committed code follows the Python guidelines, install a git pre-commit hook using
the following command:

```
pre-commit install
```

Validation checks are automatically run and must be passed before code can be merged into the default branch.
