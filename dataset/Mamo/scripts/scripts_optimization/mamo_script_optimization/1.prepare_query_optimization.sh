#!/bin/bash
cd "scripts\scripts_optimization\mamo_script_optimization"
# Define paths to the input and output files.
# Change to Complex_LP in the same way.
INPUT_PATH="data\optimization\Easy_LP\mamo_easy_lp.jsonl"
OUTPUT_PATH="You_path_for_query"

mkdir -p "$OUTPUT_PATH"
python ./1.prepare_query_optimization.py --input_path "$INPUT_PATH" --output_path "$OUTPUT_PATH"
echo "Processing_1 completed."
