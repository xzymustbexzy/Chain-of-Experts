
#!/bin/bash
# select error first
ERROR_DIR="Your_dir_for_result\lp_errors"
OUTPUT_DIR_1="Your_dir_for_result"
mkdir -p "$OUTPUT_DIR"
python ./3.5.select_error.py --error_dir "$ERROR_DIR"  --output_dir "$OUTPUT_DIR_1"

# Output a completion message.
echo "Select error completed."

MODEL_PATH="path/to/model"
NUM_GPUS=8
CUSTOM_CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

TEST_FILE="Your_dir_for_result/lp_errors_query.jsonl"

OUTPUT_DIR="Your_dir_for_fixed_data"

CUDA_VISIBLE_DEVICES=$CUSTOM_CUDA_VISIBLE_DEVICES python -m 2.run_model_lp_open \
    --model_name_or_path $MODEL_PATH \
    --tensor_parallel_size $NUM_GPUS \
    --data_file $TEST_FILE \
    --save_dir $OUTPUT_DIR \
    --topk 1 \
    --decoding sampling \
    --verbose



