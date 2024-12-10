import argparse
import time
import os
import re
from tqdm import tqdm
from pathlib import Path
from langchain.callbacks import get_openai_callback
from test_generated_code import test_generated_code, read_test_samples
from utils import extract_code_from_string, read_problem
from result import Result
import baseline.standard as standard
import baseline.chain_of_thought as cot
import baseline.progressive_hint as php
from main import chain_of_experts


algorithms = {
    'standard': standard,
    'chain_of_thought': cot,
    'cot': cot,
    'progressive_hint': php,
    'php': php,
    # 'solo_performance_prompting': ssp,
    # 'ssp': ssp,
    # 'reflexion': reflexion,
}


def main():
    parser = argparse.ArgumentParser(description='Generate and test code.')
    parser.add_argument('--dataset', type=str, help='Dataset name, "LPWP" or "ComplexOR"')
    parser.add_argument('--problem', type=str, help='Problem name')
    parser.add_argument('--algorithm', type=str, help='Algorithm name')
    parser.add_argument('--enable_reflection', action='store_true', help='Enable reflection option')
    parser.add_argument('--log_dir', type=str, default='log', help='The directory of log')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help='Base large language model')
    parser.add_argument('--max_collaborate_nums', type=int, default=3, help='Number of max collaborations')
    parser.add_argument('--max_trials', type=int, default=3, help='Maximum number of forward-backward trials')
    args = parser.parse_args()
    args.algorithm = args.algorithm.lower()

    matched_problems = []
    for p in os.listdir(os.path.join('dataset', args.dataset)):
        if re.match(args.problem, p):
            matched_problems.append(p)
    total_num = len(matched_problems)
    if total_num == 0:
        print('No problem matched! Please check arguements.')
        exit(0)

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
                algorithm = algorithms[args.algorithm]
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
            result = test_generated_code(problem, test_samples, f)

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
    print(f'Runtime error{re_num / total_num * 100:.2f}%')

if __name__ == '__main__':
    main()
