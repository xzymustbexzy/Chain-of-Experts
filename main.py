import os
import importlib
import traceback
import numpy as np
from commet import Comment
from conductor import Conductor
from reducer import Reducer
from evaluator import Evaluator
from experts import ModelingExpert, ProgrammingExpert
from comment_pool import CommentPool
from utils import extract_code_from_string
from test_generated_code import test_generated_code, read_test_samples


def evaluate(problem, samples):
    feedback = ''
    try:
        import generated_code
        importlib.reload(generated_code)
    except BaseException as e:
        feedback += 'There is grammar error in generated code!\n'
        feedback += traceback.format_exc() + '\n'
        return feedback

    try:
        func = getattr(generated_code, problem)
    except AttributeError as e:
        feedback += 'Cannot load function!\n'
        feedback += traceback.format_exc() + '\n'
        return feedback
    return None


def chain_of_experts(problem, max_collaborate_nums=5, model_name='gpt-3.5-turbo'):
    """Run Chain of Experts pipeline
    
    Args:
        problem: a dict of problem_description and code_example.
    
    Return:
        code: code of problem
    """
    all_experts = [
        ModelingExpert(model_name),
        ProgrammingExpert(model_name)
    ]
    num_experts = len(all_experts)
    reducer = Reducer(model_name)
    comment_pool = CommentPool(all_experts, visible_matrix=np.ones((num_experts, num_experts)))
    
    expert_stack = []
    for next_expert in all_experts:
        next_expert.forward(problem, comment_pool)
        comment_text = next_expert.forward(problem, comment_pool)
        comment_pool.add_comment(Comment(next_expert, comment_text))
        expert_stack.append(next_expert)
        answer = comment_text
    # answer = reducer.forward(problem, comment_pool)

    code = extract_code_from_string(answer)
    with open('generated_code.py', 'w') as f:
        f.write(code)

    dataset = 'LPWP'
    problem = 'prob_240'
    test_samples = read_test_samples(dataset, problem)
    feedback = evaluate(problem, test_samples)
    print('============== feedback ==============')
    print(feedback)

    if feedback is not None:
        while expert_stack:
            previous_expert = expert_stack.pop()
            result = previous_expert.backward(feedback)
            break
        print('=========== reflection ===========')
        print(result)

    return answer

    # num_experts = len(all_experts)

    # workspace = Workspace(all_experts, visible_matrix=np.ones((num_experts, num_experts)))

    # conductor = Conductor(model_name)
    # reducer = Reducer(model_name)
    # # evaluator = Evaluator()

    # while True:
    #     for round in range(max_collaborate_nums):
    #         print(problem)
    #         next_expert = conductor.forward(problem['description'], workspace)

    #         print(f'Round {round}, choose expert: {next_expert.name}')

    #         comment_text = next_expert.forward(problem, workspace)

    #         print(f'Give comment:\n{comment_text}')

    #         comment = Comment(next_expert, comment_text)
    #         workspace.add_comment(comment)

    #     answer = reducer.forward(problem, workspace)

    #     feedback, done = evaluator.forward(answer)
    #     if done:
    #         break
    #     found_mistake = False
    #     last_answer = answer
    #     while not found_mistake:
    #         comment = comment_set.pop_comment()
    #         expert = comment.expert
    #         feedback, found_mistake = expert.backward(problem, last_answer, feedback)
    #         last_answer = comment.comment_text

    # return answer


if __name__ == '__main__':
    from utils import read_problem
    problem = read_problem('LPWP', 'prob_240')
    chain_of_experts(problem, model_name='gpt-3.5-turbo-1106')
