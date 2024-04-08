import os
import json
import numpy as np
from comment import Comment
from conductor import Conductor
from reducer import Reducer
from evaluator import Evaluator
from experts import (
    ModelingExpert, 
    ProgrammingExpert,
    LPFileGenerator,
    ModelingKnowledgeSupplementExpert,
    ParameterExtractor,
    CodeReviewer,
    ProgrammingExampleProvider,
    TerminologyInterpreter,
)
from comment_pool import CommentPool
from utils import extract_code_from_string


def chain_of_experts(problem, 
                     max_collaborate_nums, 
                     model_name, 
                     enable_reflection,
                     max_trials):
    """Run Chain of Experts pipeline
    
    Args:
        problem: a dict of problem_description and code_example.
    
    Return:
        code: code of problem
    """
    all_experts = [
        TerminologyInterpreter(model_name),
        ParameterExtractor(model_name),
        ModelingExpert(model_name),
        ProgrammingExampleProvider(model_name),
        ProgrammingExpert(model_name),
        # LPFileGenerator(model_name),
        ModelingKnowledgeSupplementExpert(model_name),
        CodeReviewer(model_name),
    ]
    num_experts = len(all_experts)
    reducer = Reducer(model_name)
    comment_pool = CommentPool(all_experts, visible_matrix=np.ones((num_experts, num_experts)))
    conductor = Conductor(model_name)
    evaluator = Evaluator(model_name)
    expert_stack = []

    for _ in range(max_trials):
        for _ in range(max_collaborate_nums):
            next_expert = conductor.forward(problem, comment_pool, max_collaborate_nums)
            print(f'Choose next expert: {next_expert.name}')
            comment_text = next_expert.forward(problem, comment_pool)
            print(f'Given comment:\n{comment_text}')
            comment_pool.add_comment(Comment(next_expert, comment_text))
            expert_stack.append(next_expert)
        answer = reducer.forward(problem, comment_pool)

        code = extract_code_from_string(answer)
        with open('generated_code.py', 'w') as f:
            f.write(code)

        if enable_reflection:
            test_sample = evaluator.forward(problem)
            print(f'Generate test sample:\n{test_sample}')
            test_samples = [test_sample]
            feedback = evaluator.evaluate(test_samples)
            feedback_pool = CommentPool(all_experts, visible_matrix=np.ones((num_experts, num_experts)))
            feedback_pool.add_comment(Comment(evaluator, feedback))
            if feedback is not None:
                while expert_stack:
                    previous_expert = expert_stack.pop()
                    previous_comment = comment_pool.pop_comment()
                    result = previous_expert.backward(feedback_pool)
                    result = json.loads(result)
                    if result['is_caused_by_you']:
                        previous_comment.comment_text = result['refined_result']
                        expert_stack.append(previous_expert)
                        comment_pool.add_comment(previous_comment)
                        break
                    else:
                        feedback_pool.add_comment(Comment(previous_expert, result['reason']))
            else:
                break
    return answer


if __name__ == '__main__':
    from utils import read_problem
    problem = read_problem('LPWP', 'prob_250')
    chain_of_experts(problem, model_name='gpt-3.5-turbo-1106', enable_reflection=False)
