
MODEL_PATH="path/to/model"
NUM_GPUS=8
CUSTOM_CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

TEST_FILE="path/for/query"

OUTPUT_DIR="dir/for/output"

CUDA_VISIBLE_DEVICES=$CUSTOM_CUDA_VISIBLE_DEVICES python -m 2.run_model_ode_open.py \
    --model_name_or_path $MODEL_PATH \
    --tensor_parallel_size $NUM_GPUS \
    --data_file $TEST_FILE \
    --save_dir $OUTPUT_DIR \
    --topk 1 \
    --decoding sampling \
    --verbose



