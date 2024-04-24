# QA Automation Framework
This is a low-code test automation framework with which users can write test automation on yaml files without the need of having technical knowledge. 

<br>

Tech stack:
- Cypress
- Python
- Yaml
- Jinja2
- Ansible
- Docker

## Publish new image version into ghcr
### Manual local push

THe following steps describes the process of how to locally publish a framework image that can be used to locally run tests.

- Login into ghcr
    - ```docker login --username <your_username> --password <personal_access_token> ghcr.io``` 

<br>

- Build docker image
    - ```docker build . -t ghcr.io/deus-ai/qa-automation-framework:latest```

<br>

- Push the image into ghcr
    - ```docker push ghcr.io/deus-ai/qa-automation-framework:latest```

<br>

### Publishing image via gh actions

There's is currently a workflow named - Build and Push Image for CI - that builds and publish a framework image that can be used by CI pipelines to run tests.

## How to run tests
### Use the folling command to locally run the automation tests:

<br>

```docker run -t -v $PWD/automation:/app/automation --rm ghcr.io/deus-ai/qa-automation-framework:latest [OPTIONS]```

<br>

The ```[OPTIONS]``` can be replaced with one or more parameters to define some execution parameters. For detailed information on which parameters can be used, type ```-h``` or ```--help```.

### Use the folling command to run the automation tests on a CI pipeline:

<br>

```docker run -t -v ${GITHUB_WORKSPACE}/automation:/app/automation --rm ghcr.io/deus-ai/qa-automation-framework_amd64:latest [OPTIONS]```

<br>

> Notes: 
> <br>- In order to use these images and run tests, the user needs to have access to DEUS-AI org on github.
> <br>- Each time a new image version is up, it is recomended to delete the local image (not applicable to CI pipelines). 
> <br>- In case, while running the command, the following error happens:
> <br>
> <br>```docker: Error response from daemon: Head "https://ghcr.io/v2/deus-ai/qa-automation-framework/manifests/latest": unauthorized.```
> <br>``` See 'docker run --help'. ``` 
> <br>
> <br>Do a registry login with the bellow command and then try again.
> <br>
> <br>```docker login --username <your_username> --password <personal_access_token> ghcr.io/deus-ai```
> <br>
