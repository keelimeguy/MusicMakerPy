#!/bin/bash

#######################
# User Configurations
#######################

# Point to your python 3 executable
PYTHON=python

# STRONGLY RECOMMENDED!
# so long as you have pip installed: (e.g. `apt-get install python3-pip`)
# then the run script will set this up automatically
USE_VENV=yes # no|yes

#######################
#######################

print_usage () {
    echo "usage: \`$0 [help|venv|test|format|-h]\`"
    echo "  args:"
    echo "     help: prints this"
    echo "     venv: updates the virtual environment"
    echo "     test: runs the tests"
    echo "     format: runs the autoformat"
    echo "     -h: prints bot script help options"
}

validate_script_assumptions () {
    # Check python version
    if [ "$(${PYTHON} -c "import sys; print(sys.version_info[0])")" -ne 3 ]; then
        echo "This script assumes python version 3, you are using:"
        ${PYTHON} --version
        exit 1
    fi

    # Check script directory
    if [ "$(dirname $0)" != "." ]; then
        echo "This script needs to be ran from within it's own directory, e.g. \`./$(basename $0)\`"
        exit 1
    fi

    # Require at least one argument
    if [ "$#" -eq 0 ]; then
        print_usage
        exit 1
    fi
}

activate_venv () {
    if [ "${USE_VENV}" == "yes" ]; then
        if [ -f "venv/bin/activate" ]; then
            source venv/bin/activate || exit 1
        elif [ -f "venv/Scripts/activate" ]; then
            source venv/Scripts/activate || exit 1
        else
            echo "You need to first setup the virtual environment: \`$0 venv\`"
            exit 1
        fi
    elif [  "${USE_VENV}" != "no"  ]; then
        echo "invalid configuration: \"USE_VENV\" should be yes|no"
        exit 1
    fi
}

run_venv () {
    if [ "${USE_VENV}" == "yes" ]; then
        if [ ! -f "venv/Scripts/activate" ] && [ ! -f "venv/bin/activate" ]; then
            ${PYTHON} -m pip install virtualenv || exit 1
            ${PYTHON} -m virtualenv venv || exit 1

            activate_venv

            ${PYTHON} -m pip install --upgrade pip
            ${PYTHON} -m pip install flake8 pytest coverage autopep8
            ${PYTHON} -m pip install -r requirements.txt

        else
            activate_venv
            ${PYTHON} -m pip install -r requirements.txt
        fi

    else
        echo "Sorry, but your configurations specify not to use a virtual environment!"
        exit 1
    fi
}

run_test () {
    activate_venv

    flake8 musicmaker/ --count --select=E9,F63,F7,F82 --show-source --statistics
    flake8 musicmaker/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    flake8 ust_creator/ --count --select=E9,F63,F7,F82 --show-source --statistics
    flake8 ust_creator/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    coverage run --source=musicmaker,ust_creator -m pytest
    coverage report --skip-covered
}

run_format () {
    activate_venv

    for f in `find musicmaker/ -name "*.py"`; do autopep8 --in-place --max-line-length=127 $f; done
    for f in `find ust_creator/ -name "*.py"`; do autopep8 --in-place --max-line-length=127 $f; done
}

run_main () {
    activate_venv

	${PYTHON} -m musicmaker.main $@
}

##############################################

validate_script_assumptions $@

if [ "$#" -eq 1 ]; then
    if  [ "$1" == "help" ]; then
        print_usage
        exit 0

    elif [ "$1" == "venv" ]; then
        run_venv
        exit 0

    elif [ "$1" == "test" ]; then
        run_test
        exit 0

    elif [ "$1" == "format" ]; then
        run_format
        exit 0
    fi
fi

run_main $@
