#!/bin/bash


# Define paths to the input and output files.
INPUT_PATH="data/ode/mamo_ode.jsonl"
OUTPUT_PATH="path/for/query"

mkdir -p "$OUTPUT_PATH"

# Running the Python script with command-line arguments.
# Ensure python command points to the correct Python executable if not the default.
python ./1.prepare_query_ode.py --input_path "$INPUT_PATH" --output_path "$OUTPUT_PATH"
echo "Processing_1 completed."
