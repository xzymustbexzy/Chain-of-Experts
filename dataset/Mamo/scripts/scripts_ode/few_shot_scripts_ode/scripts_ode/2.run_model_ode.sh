#!/bin/bash

# Define paths to the input JSONL file and the output directory for .lp files.
INPUT_PATH="..\outputs\output_shot0"
OUTPUT_DIR="..\results\result_shot0"

# Define the path to the API keys and the model name.
KEYS_PATH="./api_keys.txt"
MODEL_NAME=""

# Define the temperature for the API model interaction.
TEMPERATURE=""

# Check if the output directory exists; if not, create it
mkdir -p "$OUTPUT_DIR"

# Run the Python script with command-line arguments.
# Ensure the python command points to the correct Python executable if not the default.
python 2.run_model_optimization.py --input_path "$INPUT_PATH" --output_dir "$OUTPUT_DIR" --keys_path "$KEYS_PATH" --model_name "$MODEL_NAME" --temperature "$TEMPERATURE"

# Output a completion message.
echo "Processing completed."
