#!/bin/bash

cd "scripts\scripts_optimization\mamo_script_optimization"

# Define the paths for data folder, output folder, and JSONL file with standard answers.
DATA_FOLDER="Your_dir_for_output"

FIX_DATA_FOLDER="Your_dir_for_fixed_data"

python ./fix_basic_error.py --data_folder "$DATA_FOLDER"
python ./fix_basic_error.py --data_folder "$FIX_DATA_FOLDER"

# Output a completion message.
echo "Processing fix_basic_error fix."

OUTPUT_FOLDER="Your_dir_for_rerun_result"

ANSWERS_PATH="data\optimization\Easy_LP\mamo_easy_lp.jsonl"

# Ensure the output folder exists.
mkdir -p "$OUTPUT_FOLDER"

# Run the Python script with predefined command-line arguments.
# Replace 'your_python_script.py' with the actual name of your Python file.
python ./5.rerun_code_comp_optimization.py --data_folder "$DATA_FOLDER" --fixed_data_folder "$FIX_DATA_FOLDER" --output_folder "$OUTPUT_FOLDER" --answers_path "$ANSWERS_PATH"
# Output a completion message.
echo "Processing and comparison of LP files completed."
