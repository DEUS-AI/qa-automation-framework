#!/bin/bash

# remove runtime folder if exists and create it from scratch
rm -rf ./runtime
mkdir runtime

# make temporary cy_tests dir to hold cypress tests after conversion from yaml files and move it to runtime dir
mkdir cy_tests && mv cy_tests runtime

# copy both source code and automation folder to runtime dir
# Move cwd to runtime dir
cp -R src/* runtime && cp -R automation runtime
cd runtime

# make cypress folder and arranje cypress basic architecture
mkdir cypress && mv templates/cyframework/* cypress && rm -rf templates/cyframework && mv cypress/cypress.config.js ./
mv automation/support/files/* cypress/fixtures


# Default values
CYPRESS_COMMAND="cypress run"
CUSTOM_ARGS=""
ENV_ARG=""
CONFIG_OPTIONS=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -h, --help          Show this help message"
            echo "  -a, --acceptance    Specify the acceptance files to run. Multiple files should be seperated with comma and to run all tests within a folder use glob (**, *)"
            echo "  -b, --browser       Specify the browser to use (e.g., chrome, firefox)" #TODO - right now only accepts electron due to the dockerfile base img (need to check)
            echo "  -c, --config        Specify custom option(s) to change on the config file"
            echo "  -e, --env           Specify cypress environment variables"
            echo "  -t, --tags          Specify the test suite or test tags to be executed. By default is none, so all tests within the project will be executed"
            exit 0
            ;;
        -a|--acceptance)
            CUSTOM_ARGS+=" --spec $2"
            shift 2
            ;;
        -b|--browser)
            CUSTOM_ARGS+=" --browser $2"
            shift 2
            ;;
        -c|--config)
            CONFIG_OPTIONS="${2/:/=}"
            shift 2
            ;;
        -e|--env)
            if [[ $ENV_ARG != "" ]]; then
                ENV_ARG+=",$2"
            else
                ENV_ARG+=" --env $2"
            fi
            shift 2
            ;;
        -t|--tags)
            if [[ $ENV_ARG != "" ]]; then
                ENV_ARG+=",grepTags=$2"
            else
                ENV_ARG+=" --env grepTags=$2"
            fi
            shift 2
            ;;
        *)
            echo "Unknown option: $1. Use -h or --help for usage information."
            exit 1
            ;;
    esac
done

# replace yml environment variables
if [[ -n "$CONFIG_OPTIONS" ]]; then 
    ansible-playbook repalceEnvVars.yml --extra-vars "$CONFIG_OPTIONS"
else
    ansible-playbook repalceEnvVars.yml
fi

# replace cypress variables
ansible-playbook replaceCyVars.yml

# run main source code file to transform all codeless automation into js cypress
# finish arranje the cypress architecture
python3 main.py && mv cy_tests/* cypress/acceptance && rm -R cy_tests


# run tests
echo $CYPRESS_COMMAND $CUSTOM_ARGS $ENV_ARG && $CYPRESS_COMMAND $CUSTOM_ARGS $ENV_ARG

# generate test execution html report and process its location
# NOTE: when running with docker a volume with root level must be mounted
rm -rf ./../automation/report 2>/dev/null || true
mv cypress/report ./../automation 
[ -d "cypress/logs" ] && cp -R cypress/logs ./../automation/report/failures 
