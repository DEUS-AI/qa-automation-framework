# automation-framework
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

- Login into ghcr
    - ```docker login --username <your_username> --password <personal_access_token> ghcr.io``` 

<br>

- Build docker image
    - ```docker build . -t ghcr.io/deus-ai/qa-automation-framework:latest```

<br>

- Push the image into ghcr
    - ```docker push ghcr.io/deus-ai/qa-automation-framework:latest```

<br>

> Note: Whenever a push is done to the reposotory main branch, a github action will automatically trigger to build a new image and publish it on ghcr.


## How to run tests
Use the folling command to run the automation tests:

<br>

```docker run -t -v $PWD/automation:/app/automation --rm ghcr.io/deus-ai/qa-automation-framework:latest [OPTIONS]```

<br>

The [OPTIONS] can be replaced with one or more of the following arguments to define some execution parameters:
- -h or --help
    - will not run anything but provide the usage method of this command.
- -b or --browser
    - Specifies the browser where web test cases should run. Default is electon (cypress default browser)
- ... TBD ...

<br>

> Note: in order to use this image and run tests, the user needs to have access to DEUS-AI org on github.


