#!/bin/bash

cd "scripts/scripts_ode/mamo_script_ode"

# Define the paths for data folder, output folder, and JSONL file with standard answers.
DATA_FOLDER="dir/for/output"
FIX_DATA_FOLDER="dir/for/fixed/data"
OUTPUT_FOLDER="dir/for/rerun/result"
ANSWERS_PATH="data/ode/mamo_ode.jsonl"

# Ensure the output folder exists.
mkdir -p "$OUTPUT_FOLDER"

python ./fix_basic_error.py --data_folder "$FIX_DATA_FOLDER"

# Output a completion message.
echo "Processing fix_basic_error."
# Run the Python script with predefined command-line arguments.
# Replace 'your_python_script.py' with the actual name of your Python file.
python ./5.rerun_code_comp_ode.py --data_folder "$DATA_FOLDER" --fixed_data_folder "$FIX_DATA_FOLDER" --output_folder "$OUTPUT_FOLDER" --answers_path "$ANSWERS_PATH"

# Output a completion message.
echo "Processing and comparison of python files completed."
