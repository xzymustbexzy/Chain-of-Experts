#!/bin/bash
cd "scripts\scripts_optimization\mamo_script_optimization"


# Define paths to the input JSONL file and the output directory for .lp files.
INPUT_PATH="Your_path_for_query"
OUTPUT_DIR="Your_dir_for_output"

# Define the path to the API keys and the model name.
KEYS_PATH="api_keys.txt"
MODEL_NAME=""

# Define the temperature for the API model interaction.
TEMPERATURE=""

# Check if the output directory exists; if not, create it
mkdir -p "$OUTPUT_DIR"

# Run the Python script with command-line arguments.
# Ensure the python command points to the correct Python executable if not the default.
python ./2.run_model_optimization.py --input_path "$INPUT_PATH" --output_dir "$OUTPUT_DIR" --keys_path "$KEYS_PATH" --model_name "$MODEL_NAME" --temperature "$TEMPERATURE"

# Output a completion message.
echo "Processing_2 completed."
