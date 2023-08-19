#!/bin/bash

read_cli_result() {
    # Get the system's temporary directory using Python
    local temp_dir=$(python3 -c "import tempfile; print(tempfile.gettempdir())")

    local result_file_path="${temp_dir}/swiftly_cli_result.txt"
    
    # Check if the result file exists
    if [[ ! -f "$result_file_path" ]]; then
        echo "Error: Result file not found!"
        return 1
    fi
    
    # Read the result
    local result=$(cat "$result_file_path")
    
    # Remove the temporary file
    rm "$result_file_path"
    
    # Return the result
    echo "$result"
}

is_sourced() {
    # If the script's parent process is the same as the current shell, then it's being sourced
    # $0 is the name of the script, and $BASH_SOURCE is the source of the current script
    [[ "$0" != "$BASH_SOURCE" ]]
    echo "is_sourced: $0 vs $BASH_SOURCE"  # Add this line for debugging
}

ensure_sourced(){
    # Check if the script is being sourced
    if ! is_sourced; then
        echo "Script is not being sourced."
        echo "Please run this script using 'source' or '.'"
        return 1 2>/dev/null || exit 1  # If sourced, use 'return'. If run as a script, use 'exit'.
    else
        echo "Script is being sourced."
    fi
}