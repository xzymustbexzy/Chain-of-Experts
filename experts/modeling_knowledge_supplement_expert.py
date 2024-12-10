from experts.base_expert import BaseExpert

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI


class ModelingKnowledgeSupplementExpert(BaseExpert):

    ROLE_DESCRIPTION = 'You are an experts that offers supplementary knowledge related to modeling techniques and best practices.'
    FORWARD_TASK = '''You are given a specific problem. You aim to develop an efficient Python program that addresses the given problem.
Now the origin problem is as follow:
{problem_description}
Let's analyse the problem step by step, and then give your Python code.
Here is a starter code:
{code_example}
And the comments from other experts are as follow:
{comments_text}

Give your Python code directly.'''
    BACKWARD_TASK = '''When you are solving a problem, you get a feedback from the external environment. You need to judge whether this is a problem caused by you or by other experts (other experts have given some results before you). If it is your problem, you need to give Come up with solutions and refined code.

The original problem is as follow:
{problem_description}

The code you give previously is as follow:
{previous_code}
    
The feedback is as follow:
{feedback}

The output format is a JSON structure followed by refined code:
{{
    'is_caused_by_you': false,
    'reason': 'leave empty string if the problem is not caused by you',
    'refined_result': 'Your refined code...'
}}
'''

    def __init__(self, model):
        super().__init__(
            name='Modeling Knowledge Supplement Expert',
            description='Skilled in programming and coding, capable of implementing the optimization solution in a programming language.',
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
        print('-' * 30)
        print('Input of programming expert:')
        print(self.forward_prompt_template.format(
            problem_description=problem['description'], 
            code_example=problem['code_example'],
            comments_text=comments_text))
        output = self.forward_chain.predict(
            problem_description=problem['description'], 
            code_example=problem['code_example'],
            comments_text=comments_text
        )
        print()
        print('Output of programming expert:')
        print(output)
        print()
        self.previous_code = output
        return output

    def backward(self, feedback_pool):
        if not hasattr(self, 'problem'):
            raise NotImplementedError('Please call foward first!')
        output = self.backward_chain.predict(
            problem_description=self.problem['description'], 
            previous_code=self.previous_code,
            feedback=feedback_pool.get_current_comment_text())
        return output
