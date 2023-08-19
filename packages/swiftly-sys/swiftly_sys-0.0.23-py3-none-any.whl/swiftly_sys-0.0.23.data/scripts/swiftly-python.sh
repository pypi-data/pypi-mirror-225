#!/bin/bash

activate_python() {
    # Get the project name from the environment variable
    local project_name="$SWIFTLY_PROJECT_NAME"

    # Check if the virtual environment exists
    if [[ ! -d "venv${project_name}" ]]; then
        echo "Error: Virtual environment 'venv${project_name}' not found."
        return 1
    fi

    # Source the virtual environment's activate script
    source "venv${project_name}/bin/activate"

    # Install the requirements using the Python function
    python3 -c "from swiftly.runtime.python.main import install_requirements; install_requirements()"
}

deactivate_python() {
    # Check if the virtual environment is activated
    if [[ -z "$VIRTUAL_ENV" ]]; then
        echo "Error: No virtual environment is currently activated."
        return 1
    fi

    # Deactivate the virtual environment
    deactivate
}


run(){
    echo "running python"
}

custom() {
    echo "Running python custom function with arguments: $@"
    # Add your custom command handling logic here
}

# Check if a function exists and call it, otherwise call the custom function
if declare -f "$1" > /dev/null; then
    "$@"
else
    # Check if there's more than one argument
    if [ $# -gt 1 ]; then
        custom "${@:2}"  # Pass all arguments except the first one to custom
    fi
fi
