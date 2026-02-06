import os
import json
import importlib
from result import Result


class NullWriter:
    def write(self, s):
        pass

def test_generated_code(problem, samples, log_file=None, dataset='ComplexOR'):
    log_file = log_file or NullWriter()

    with open(f'gt_programs/{problem}.py', 'r', encoding='utf8') as f:
        program = f.read()
    with open('generated_code.py', 'w', encoding='utf8') as f:
        f.write(program)

    try:
        import generated_code
        importlib.reload(generated_code)
    except BaseException as e:
        log_file.write('There is grammar error in generated code!\n')
        log_file.write(str(e) + '\n')
        return Result.COMPILE_ERROR

    try:
        func = getattr(generated_code, problem)
    except AttributeError as e:
        log_file.write('Cannot load function!\n')
        log_file.write(str(e) + '\n')
        return Result.COMPILE_ERROR

    post_process = None
    if os.path.exists(os.path.join('dataset', dataset, problem, 'data_process.py')):
        data_process = importlib.import_module(f'dataset.{dataset}.{problem}.data_process')
        if hasattr(data_process, 'post_process'):
            post_process = data_process.post_process

    total_num = len(samples)
    passed_num = 0
    is_re = False
    for i, sample in enumerate(samples):
        try:
            output = func(**sample['input'])
        except BaseException as e:
            is_re = True
            log_file.write('Runtime Error\n')
            log_file.write(str(e))
            continue
        if post_process is not None:
            output = post_process(*output)
        
        if len(sample['output']) == 1:
            ground_truth = sample['output'][0]
        else:
            ground_truth = tuple(sample['output'])

        print('=' * 20)
        print(output)
        print(ground_truth)
        print()
        log_file.write('Program Output:\n')
        log_file.write(str(output))
        is_passed = (output == ground_truth)
        if is_passed:
            passed_num += 1
        # assert output == tuple(sample['output']), f'Test failed:\nprogram output: {output}\nground truth: {tuple(sample["output"])}'
    # print('Test passed!!!')
    is_correct = (passed_num == total_num)

    if is_re:
        return Result.RUNTIME_ERROR
    if is_correct:
        return Result.ACCEPT
    else:
        return Result.WRONG_ANSWER


def read_test_samples(dataset, problem):
    with open(os.path.join('dataset', dataset, problem, 'sample.json'), 'r', encoding='utf8') as f:
        test_samples = json.load(f)
    return test_samples


if __name__ == '__main__':
    dataset = 'ComplexOR'
    for filename in os.listdir('gt_programs'):
        if not filename.endswith('.py'):
            continue
        problem = filename[:-3]
        test_samples = read_test_samples(dataset, problem)
        with open(f'gt_program_result/{problem}.txt', 'w') as f:
            test_generated_code(problem, test_samples, log_file=f, dataset=dataset)
