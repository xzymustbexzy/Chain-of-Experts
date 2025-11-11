#!/bin/bash

cd "scripts/scripts_ode/mamo_script_ode"

ERROR_DIR="dir/for/result/errors"
FILE_PATH="file/path/for/error/info"
OUTPUT_DIR="dir/for/fixed/data"

# Define the path to the API keys and the model name.
KEYS_PATH="./api_keys.txt"
MODEL_NAME=""

# Define the temperature for the API model interaction.
TEMPERATURE="0"

# Check if the output directory exists; if not, create it
mkdir -p "$OUTPUT_DIR"

# Run the Python script with command-line arguments.
# Ensure the python command points to the correct Python executable if not the default.
python ./4.fix_error_ode.py --error_dir "$ERROR_DIR" --file_path "$FILE_PATH" --output_dir "$OUTPUT_DIR" --keys_path "$KEYS_PATH" --model_name "$MODEL_NAME" --temperature "$TEMPERATURE"

# Output a completion message.
echo "Processing completed."
