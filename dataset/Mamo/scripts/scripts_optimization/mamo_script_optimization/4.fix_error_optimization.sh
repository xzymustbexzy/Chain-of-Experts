#!/bin/bash

cd "D:\code\AI_for_Math\benchmark_for_modeling\dataset(benchmark)\benchmark_scripts_optimization_complex\code_optimization"

ERROR_DIR="Your_dir_for_result\lp_errors"
OUTPUT_DIR="Your_dir_for_fixed_data"

KEYS_PATH=""
MODEL_NAME=""

TEMPERATURE="0.8"

mkdir -p "$OUTPUT_DIR"

python ./4.fix_error_optimization.py --error_dir "$ERROR_DIR"  --output_dir "$OUTPUT_DIR" --keys_path "$KEYS_PATH" --model_name "$MODEL_NAME" --temperature "$TEMPERATURE"

echo "Processing completed."
