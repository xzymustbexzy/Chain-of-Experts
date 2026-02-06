import argparse
import time
import os
import re
import importlib
from tqdm import tqdm
from pathlib import Path
from langchain_community.callbacks.manager import get_openai_callback
from test_generated_code import test_generated_code, read_test_samples
from utils import extract_code_from_string, read_problem
from result import Result
from main import chain_of_experts


algorithms = {
    'standard': 'baseline.standard',
    'chain_of_thought': 'baseline.chain_of_thought',
    'cot': 'baseline.chain_of_thought',
    'progressive_hint': 'baseline.progressive_hint',
    'php': 'baseline.progressive_hint',
}


def main():
    parser = argparse.ArgumentParser(description='Generate and test code.')
    parser.add_argument('--dataset', type=str, required=True, help='Dataset name, "LPWP" or "ComplexOR"')
    parser.add_argument('--problem', type=str, required=True, help='Problem name regex')
    parser.add_argument(
        '--algorithm',
        type=str,
        required=True,
        choices=['standard', 'chain_of_thought', 'cot', 'progressive_hint', 'php', 'chain_of_experts', 'coe'],
        help='Algorithm name',
    )
    parser.add_argument('--enable_reflection', action='store_true', help='Enable reflection option')
    parser.add_argument('--log_dir', type=str, default='log', help='The directory of log')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help='Base large language model')
    parser.add_argument('--max_collaborate_nums', type=int, default=3, help='Number of max collaborations')
    parser.add_argument('--max_trials', type=int, default=3, help='Maximum number of forward-backward trials')
    args = parser.parse_args()
    args.algorithm = args.algorithm.lower()
    if args.max_collaborate_nums <= 0:
        parser.error('--max_collaborate_nums must be a positive integer')
    if args.max_trials <= 0:
        parser.error('--max_trials must be a positive integer')

    dataset_dir = os.path.join('dataset', args.dataset)
    if not os.path.isdir(dataset_dir):
        parser.error(f'Dataset not found: {dataset_dir}')

    try:
        problem_pattern = re.compile(args.problem)
    except re.error as exc:
        parser.error(f'Invalid problem regex: {exc}')

    matched_problems = []
    for p in os.listdir(dataset_dir):
        if problem_pattern.match(p) and os.path.isdir(os.path.join(dataset_dir, p)):
            matched_problems.append(p)
    matched_problems.sort()
    total_num = len(matched_problems)
    if total_num == 0:
        parser.error('No problem matched. Please check --problem and --dataset.')

    Path(args.log_dir).mkdir(parents=True, exist_ok=True)
    log_dir_name = f'run_{args.algorithm}_{args.dataset}_{str(round(time.time()))}'
    path = os.path.join(args.log_dir, log_dir_name)
    print(f'Save log to {path}')
    Path(path).mkdir(parents=True, exist_ok=True)

    correct_num = 0
    ce_num = 0
    re_num = 0
    pbar = tqdm(total=len(matched_problems))
    current_num = 0
    for problem in matched_problems:
        problem_data = read_problem(args.dataset, problem)
        with get_openai_callback() as cb:
            if args.algorithm == 'chain_of_experts' or args.algorithm == 'coe':
                answer = chain_of_experts(
                    problem_data, 
                    args.max_collaborate_nums, 
                    model_name=args.model, 
                    enable_reflection=args.enable_reflection,
                    max_trials=args.max_trials)
                time.sleep(10)
            else:
                algorithm_module = importlib.import_module(algorithms[args.algorithm])
                algorithm = algorithm_module
                answer = algorithm.solve(problem_data, model_name=args.model)
            print('-' * 10 + 'Token usage' + '-' * 20)
            print(cb)
            print('-' * 25)
        
        with open(os.path.join(path, f'{problem}_original_answer.txt'), 'w', encoding='utf8') as f:
            f.write(answer)
        
        code = extract_code_from_string(answer)
        
        with open(os.path.join(path, f'{problem}_generated_code.py'), 'w', encoding='utf8') as f:
            f.write(code)

        with open('generated_code.py', 'w') as f:
            f.write(code)

        test_samples = read_test_samples(args.dataset, problem)
        with open(os.path.join(path, f'{problem}_test_log.txt'), 'w', encoding='utf8') as f:
            result = test_generated_code(problem, test_samples, f, dataset=args.dataset)

        if result == Result.ACCEPT:
            correct_num += 1
        elif result == Result.COMPILE_ERROR:
            ce_num += 1
        elif result == Result.RUNTIME_ERROR:
            re_num += 1
        
        pbar.update()
        current_num += 1
        pbar.set_description(f'Accuracy: {correct_num / current_num * 100:.2f}% | Compile error: {ce_num / current_num * 100:.2f}% | Runtime error: {re_num / current_num * 100:.2f}%')

    print(f'Passed: {correct_num}/{total_num}')
    print(f'Accuracy: {correct_num / total_num * 100:.2f}%')
    print(f'Compile error: {ce_num / total_num * 100:.2f}%')
    print(f'Runtime error: {re_num / total_num * 100:.2f}%')

if __name__ == '__main__':
    main()
