import os
import json
import importlib
from result import Result


class NullWriter:
    def write(self, s):
        pass

def test_generated_code(problem, samples, log_file=None):
    log_file = log_file or NullWriter()

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
    if os.path.exists(os.path.join('dataset', problem, 'data_process.py')):
        data_process = importlib.import_module('dataset.' + problem + '.data_process')
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
            log_file.write('=' * 15 + f'test sample {i}' + '=' * 15 + '\n')
            log_file.write('Runtime Error\n')
            log_file.write(str(e) + '\n\n')
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
        log_file.write('=' * 15 + f'test sample {i}' + '=' * 15 + '\n')
        log_file.write('Program Output:\n')
        log_file.write(str(output) + '\n\n')
        log_file.write('Ground Truth:\n')
        log_file.write(str(ground_truth) + '\n')
        is_passed = (output == ground_truth)
        if is_passed:
            passed_num += 1
        log_file.write(f'Is passed: {is_passed}\n')
        log_file.write('\n')
        # assert output == tuple(sample['output']), f'Test failed:\nprogram output: {output}\nground truth: {tuple(sample["output"])}'
    # print('Test passed!!!')
    log_file.write('\n\n')
    log_file.write(f'{passed_num}/{total_num} passed\n')
    is_correct = (passed_num == total_num)
    log_file.write(f'is correct: {is_correct}\n')

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
    dataset = 'LPWP'
    problem = 'prob_245'
    test_samples = read_test_samples(dataset, problem)
    test_generated_code(problem, test_samples)
