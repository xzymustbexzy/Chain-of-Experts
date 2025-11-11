#!/bin/bash

# Define the paths for data folder, output folder, and JSONL file with standard answers.
DATA_FOLDER="..\results\result_shot0"
OUTPUT_FOLDER="..\results_error\result_error_shot0"
ANSWERS_PATH="..\select_data\ode_select.jsonl"

# Ensure the output folder exists.
mkdir -p "$OUTPUT_FOLDER"

# Run the Python script with predefined command-line arguments.
# Replace 'your_python_script.py' with the actual name of your Python file.
python 3.run_code_comp_ode.py --data_folder "$DATA_FOLDER" --output_folder "$OUTPUT_FOLDER" --answers_path "$ANSWERS_PATH"

# Output a completion message.
echo "Processing and comparison of python files completed."
