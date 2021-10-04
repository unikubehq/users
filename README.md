<p align="center">
  <img src="https://raw.githubusercontent.com/unikubehq/users/main/logo_users.png" width="400">
</p>
<p align="center">
    <a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
</p>

# Unikube Users Service

This is the *UNIKUBE* User-Service.

## Development Setup
We're using [black](https://github.com/psf/black). It helps us keep the code style
aligned throughout the project.

To make sure your code is well formatted, please install [pre-commit](https://pre-commit.com/). 
After that just run `pre-commit install` in the repositories root directory.

### Release

We're using [python-semantic-release](https://github.com/relekang/python-semantic-release)
for the release workflow. To publish a new version of the service, simply run
```shell
semantic-release publish
```

Write access to the repository is needed.
