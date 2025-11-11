#!/bin/bash

# Define paths to the input and output files.
# You can adjust these paths as necessary or pass them as command-line arguments to the Bash script.
INPUT_PATH="..\select_data\ode_select.jsonl"
OUTPUT_PATH="..\outputs\output_shot0.jsonl"

mkdir -p "$OUTPUT_PATH"

# Running the Python script with command-line arguments.
# Ensure python command points to the correct Python executable if not the default.
python 1.prepare_query_ode.py --input_path "$INPUT_PATH" --output_path "$OUTPUT_PATH"
echo "Processing_1 completed."
