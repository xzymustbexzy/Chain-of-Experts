import json
from experts.base_expert import BaseExpert

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI


class TerminologyInterpreter(BaseExpert):

    ROLE_DESCRIPTION = 'You are a terminology interpreter who provides additional domain-specific knowledge to enhance problem understanding and formulation.'
    FORWARD_TASK = '''As a domain knowledge terminology interpreter, your role is to provide additional information and insights related to the problem domain. 
Here are some relevant background knowledge about this problem: {knowledge}. 

You can contribute by sharing your expertise, explaining relevant concepts, and offering suggestions to improve the problem understanding and formulation. 
Please provide your input based on the given problem description: 
{problem_description}

Your output format should be a JSON like this (choose at most 3 hardest terminology):
[
  {{
    "terminology": "...",
    "interpretation": "..."
  }}
]
'''

    BACKWARD_TASK = '''When you are solving a problem, you get a feedback from the external environment. You need to judge whether this is a problem caused by you or by other experts (other experts have given some results before you). If it is your problem, you need to give Come up with solutions and refined code.

The original problem is as follow:
{problem_description}

The feedback is as follow:
{feedback}

The answer you give previously is as follow:
{previous_answer}

The output format is a JSON structure followed by refined code:
{{
    'is_caused_by_you': false,
    'reason': 'leave empty string if the problem is not caused by you',
    'refined_result': 'Your refined result'
}}
'''

    def __init__(self, model):
        super().__init__(
            name='Terminology Interpreter',
            description='Provides additional domain-specific knowledge to enhance problem understanding and formulation.',
            model=model   
        )
        self.llm = ChatOpenAI(
            model_name=model,
            temperature=0
        )
        self.forward_prompt_template = self.ROLE_DESCRIPTION + '\n' + self.FORWARD_TASK
        self.forward_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(self.forward_prompt_template)
        )
        self.backward_prompt_template = self.ROLE_DESCRIPTION + '\n' + self.BACKWARD_TASK
        self.backward_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(self.backward_prompt_template)
        )

    def forward(self, problem, comment_pool):
        self.problem = problem
        comments_text = comment_pool.get_current_comment_text()
        print('Input')
        print(self.FORWARD_TASK.format(
            problem_description=problem['description'], 
            knowledge='None',
            comments_text=comments_text
        ))
        print()
        output = self.forward_chain.predict(
            problem_description=problem['description'], 
            knowledge='None',
            comments_text=comments_text
        )
        output = json.loads(output)
        answer = ''
        for item in output:
            answer += item['terminology'] + ':' + item['interpretation'] + '\n'
        self.previous_answer = answer
        return answer

    def backward(self, feedback_pool):
        if not hasattr(self, 'problem'):
            raise NotImplementedError('Please call foward first!')
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
    expert = TerminologyInterpreter('gpt-3.5-turbo')
    answer = expert.forward(problem, comment_pool)
    print(answer)
