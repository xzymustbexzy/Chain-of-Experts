import json
import importlib
import traceback
import inspect

from experts.base_expert import BaseExpert


class Evaluator(BaseExpert):

    ROLE_DESCRIPTION = '''You are an evaluator.'''
    FORWARD_TASK = '''You will be responsible for generating test samples for verifying the correctness of a program.

You will be given an operations research optimization problem and its function signature, and you are responsible for generating an input example for testing the function.
The test data you generate must be reasonable, solvable, and realistic.
Output JSON directly without any other information!

Input:
problem: A candy store mixes regular candy and sour candy to prepare two products, regular mix and sour surprise mix. Each kilogram of the regular mix contains 0.8 kg of regular candy and 0.2 kg of sour candy. The profit per kilogram of the regular mix is $3. Each kilogram of the sour surprise mix contains 0.1 kg of regular candy and 0.9 kg of sour candy. The profit per kilogram of the sour surprise mix is $5. The candy store has 80 kg of regular candy and 60 kg of sour candy available. How many kilograms of each type of candy mix should be created to maximize profits?
code:
def prob_29(regular_mix, sour_surprise_mix, constraint1, constraint2):
    """
    Args:
        regular_mix: a float, the amount of regular mix candy created
        sour_surprise_mix: a float, the amount of sour surprise mix candy created
        constraint1: an integer, the limit of available regular candy
        constraint2: an integer, the limit of available sour candy
    Returns:
        obj: a float, the maximum profit achieved
    """
    obj = 1e9
    # To be implemented
    return obj

Output:
{{
    "input": {{
        "regular_mix": 94.2,
        "sour_surprise_mix": 45.7,
        "constraint1": 80,
        "constraint2": 60
    }}
}}

Input:
problem: {problem_description}
code:
{code_example}

Output:
'''

    def __init__(self, model):
        super().__init__(
            name='Evaluator',
            description='An special expert that generates the test data and test correctness.',
            model=model
        )

    def forward(self, problem):
        answer = self.forward_chain.predict(
            problem_description=problem['description'], 
            code_example=problem['code_example'],
        )
        answer = answer.strip("'").strip('')
        answer = json.loads(answer)
        return answer
    
    def evaluate(self, samples):
        feedback = ''
        try:
            import generated_code
            importlib.reload(generated_code)
        except BaseException as e:
            feedback += 'There is grammar error in generated code!\n'
            feedback += traceback.format_exc() + '\n'
            return feedback

        func = None
        for name, obj in inspect.getmembers(generated_code):
            if not name.startswith('prob_'):
                continue
            if inspect.isfunction(obj):
                func = obj
                print(f'Function found: {name}')
                break
        if func is None:
            raise NotImplementedError('Function not found in generated code!')
        
        for i, sample in enumerate(samples):
            try:
                func(**sample['input'])
            except BaseException as e:
                feedback += 'Runtime error!\n'
                feedback += traceback.format_exc() + '\n'
                return feedback
        
        return None
