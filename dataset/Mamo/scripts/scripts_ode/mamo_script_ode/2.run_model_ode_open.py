import argparse
import json
import os
import re
import sys

from vllm import LLM, SamplingParams
from tqdm import tqdm




# here data file is the query, can be feed to model directly

def main(args):
    assert args.data_file is not None
    assert isinstance(args.topk, int)
    assert args.decoding_method in ["greedy", "sampling"]

    if args.save_dir is None:
        args.save_dir = os.path.join("results", args.model_name_or_path.replace("/", ".").strip(".") + f".{args.prompt_template}" + f".topk_{args.topk}.{args.decoding_method}_decoding")
    os.makedirs(args.save_dir, exist_ok=True)

    # Load data
    # print(f"args.prompt_template: {args.prompt_template}")
    sample = []
    with open(args.data_file, "r", encoding='utf-8') as fd:
        for line in fd:
            example = json.loads(line)
            example_t = {k: v for k, v in example.items() if k not in ["query"]}
            prompt = example["query"]
            example_t["prompt"] = prompt
            sample.append(example_t)
    print(f"load data from `{args.data_file}` done. len(sample): {len(sample)}")

    # Init model
    model = LLM(model=args.model_name_or_path, tensor_parallel_size=args.tensor_parallel_size, trust_remote_code=True)
    print("init model done.")
    stop_tokens = ["</s>"]
    if args.decoding_method == "greedy":
        sampling_params = SamplingParams(n=args.topk, temperature=0, top_p=1,  max_tokens=4096, stop=stop_tokens) #model.llm_engine.model_config.max_model_len
    elif args.decoding_method == "sampling":
        sampling_params = SamplingParams(n=args.topk, temperature=0.8, top_p=1,  max_tokens=4096, stop=stop_tokens)
    else:
        raise
    print(f"init sampling params done: {sampling_params}")

    # generate
    prompts = [example["prompt"] for example in sample]


    num_total = 0
    for item, prompt in zip(sample, prompts):
        file_id = item['id']
        generation = model.generate(prompt, sampling_params)
        output = generation[0].outputs[0]
        output = output.text 
        save_file = os.path.join(args.save_dir, f"ode_code_{file_id}.py")
        num_total += 1
        fw = open(save_file, "w")
        fw.write(output)
        

        fw.close()
    print(f"Total outputs: {num_total}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str, default=None)  # model path
    parser.add_argument("--data_file", type=str)  # data path
    parser.add_argument("--save_dir", type=str, default=None)  # data path
    parser.add_argument("--tensor_parallel_size", type=int, default=8)  # num_gpus
    parser.add_argument("--topk", type=int, default=1)  # num_gpus
    parser.add_argument("--decoding_method", type=str, default="greedy")  # num_gpus
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args)