MVF is a pluggable ML/statistical modelling framework that allows for the easy comparison of regression models implemented in Python and R. Write simple wrapper classes for your models and compare their performance on a particular dataset. The framework executes incrementally by default, meaning you can easily add a new model, without refitting existing models.

**Pluggable** - Quickly add a new model. Easily switch-out a dataset.

**Auditable** - All results are archived. All processes are transparent.

**Reproducible** - All non-stochastic processes are reproducible. Stochastic processes are repeatable.

MVF seeks to bridge the gap between R&D and integration with production applications.

## Getting started

For full documentation of the project and instructions on how to get started, visit the [documentation site](https://tomkimcta.gitlab.io/model-validation-framework).

## Main features

* Automates the supervised ML workflow with simple configuration.
* R and Python models can be plugged in easily.

## For developers

### Dependencies

You need Python>=3.9 and R>=4.0. 

Additionally, you must have a working installation of the `R6`, [`IRkernel`](https://github.com/IRkernel/IRkernel) and `arrow` R packages to leverage the R/Python interoperability.

### Git

This project operates using two Git branches

- dev
- main

All development work should be undertaken on the development branch. The dev branch should then be merged into the master branch to deploy a new version of the package. 

### CI/CD

This project uses GitLab CI/CD. Current jobs:

* **test_dev** - Runs all tests except functional tests using [pytest](https://docs.pytest.org). Runs on commits to `dev` branch.
* **test_main** - Runs all tests using [pytest](https://docs.pytest.org). Runs on commits to `main` branch.
* **build_deploy_package** - Builds the Python package and deploys to [PyPI](https://pypi.org/). Runs on commits to `main` branch.
* **build_deploy_docs** - Builds the documentation site and deploys to [GitLab Pages](https://docs.gitlab.com/ee/user/project/pages/). Runs on commits to `main` branch.

All CI/CD stages run in a Docker container. This project uses `node:latest` for the **build_deploy_docs** stage and a custom R/Python container specified by the Dockerfile for the remaining stages.

#### Docker

To update the container in the registry, navigate to the project root and run

```
sudo docker login registry.gitlab.com
```

Enter your GitLab username and password (only for members of the project). Then run

```
sudo docker build -t registry.gitlab.com/tomkimcta/model-validation-framework .
sudo docker push registry.gitlab.com/tomkimcta/model-validation-framework
```

#### PyPI

The version stored in the `version` file must be incremented for a deployment of the package to be successful.

### Documentation

This project uses a static site generator called [Docusaurus](https://docusaurus.io) to create its documentation. The content for the documentation site is contained in `documentation/docs/`. Any updates to documentation can be verified in a development server by running `npm i && npm start` from the `documentation/` directory.

