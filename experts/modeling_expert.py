from experts.base_expert import BaseExpert

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI


class ModelingExpert(BaseExpert):

    ROLE_DESCRIPTION = 'You are a modeling expert specialized in the field of Operations Research and Optimization. Your expertise lies in Mixed-Integer Programming (MIP) models, and you possess an in-depth understanding of various modeling techniques within the realm of operations research. At present, you are given an Operations Research problem, alongside additional insights provided by other experts. The goal is to holistically incorporate these inputs and devise a comprehensive model that addresses the given production challenge.'

    FORWARD_TASK = '''Now the origin problem is as follow:
{problem_description}
And the comments from other experts are as follow:
{comments_text}

Give your MIP model of this problem. Additionally, please note that your model needs to be a solvable linear programming model or a mixed-integer programming model. This also means that the expressions of the constraint conditions can only be equal to, greater than or equal to, or less than or equal to (> or < are not allowed to appear and should be replaced to be \geq or \leq).

Your output format should be a JSON like this:
{{
    "VARIABLES": "A mathematical description about variables",
    "CONSTRAINS": "A mathematical description about constrains",
    "OBJECTIVE": "A mathematical description about objective"
}}
'''

    BACKWARD_TASK = '''When you are solving a problem, you get a feedback from the external environment. You need to judge whether this is a problem caused by you or by other experts (other experts have given some results before you). If it is your problem, you need to give Come up with solutions and refined code.

The original problem is as follow:
{problem_description}

The feedback is as follow:
{feedback}

The modeling you give previously is as follow:
{previous_answer}

The output format is a JSON structure followed by refined code:
{{
    "is_caused_by_you": false,
    "reason": "leave empty string if the problem is not caused by you",
    "refined_result": "Your refined result"
}}
'''

    def __init__(self, model):
        super().__init__(
            name='Modeling Expert',
            description='Proficient in constructing mathematical optimization models based on the extracted information.',
            model=model  
        )

    def forward(self, problem, comment_pool):
        self.problem = problem
        comments_text = comment_pool.get_current_comment_text()
        print('Input')
        print(self.FORWARD_TASK.format(
            problem_description=problem['description'], 
            comments_text=comments_text
        ))
        print()
        output = self.forward_chain.predict(
            problem_description=problem['description'], 
            comments_text=comments_text
        )
        # Meet the rule of MIP
        output = output.replace(' < ', ' \leq ').replace(' > ', ' \geq ')
        self.previous_answer = output
        return output

    def backward(self, feedback_pool):
        if not hasattr(self, 'problem'):
            raise NotImplementedError('Please call forward first!')
        output = self.backward_chain.predict(
            problem_description=self.problem['description'], 
            previous_answer=self.previous_answer,
            feedback=feedback_pool.get_current_comment_text())
        return output


if __name__ == '__main__':
    from comment_pool import CommentPool
    import numpy as np
    num_experts = 0
    all_experts = []
    problem = {
        'description': 'A telecom company needs to build a set of cell towers to provide signal coverage for the inhabitants of a given city. A number of potential locations where the towers could be built have been identified. The towers have a fixed range, and due to budget constraints only a limited number of them can be built. Given these restrictions, the company wishes to provide coverage to the largest percentage of the population possible. To simplify the problem, the company has split the area it wishes to cover into a set of regions, each of which has a known population. The goal is then to choose which of the potential locations the company should build cell towers on in order to provide coverage to as many people as possible. Please formulate a mathematical programming model for this problem based on the description above.',
    }
    comment_pool = CommentPool(all_experts, visible_matrix=np.ones((num_experts, num_experts)))
    expert = ModelingExpert('gpt-3.5-turbo')
    answer = expert.forward(problem, comment_pool)
    print(answer)
