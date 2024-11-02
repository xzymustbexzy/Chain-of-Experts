from experts.base_expert import BaseExpert

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI


class ParameterExtractor(BaseExpert):

    ROLE_DESCRIPTION = 'You are an expert that identifies and extracts relevant variables from the problem state- ment.'
    FORWARD_TASK = '''As a parameter extraction expert, your role is to identify and extract the relevant variables, constrans, objective from the problem statement. 
Your expertise in the problem domain will help in accurately identifying and describing these variables. 
Please review the problem description and provide the extracted variables along with their definitions: 
{problem_description}

And the comments from other experts are as follow:
{comments_text}

Please note that the information you extract is for the purpose of modeling, which means your variables, constraints, and objectives need to meet the requirements of a solvable LP or MIP model. Within the constraints, the comparison operators must be equal to, greater than or equal to, or less than or equal to (> or < are not allowed to appear and should be replaced to be \geq or \leq).
'''
    BACKWARD_TASK = '''When you are solving a problem, you get a feedback from the external environment. You need to judge whether this is a problem caused by you or by other experts (other experts have given some results before you). If it is your problem, you need to give Come up with solutions and refined code.

The original problem is as follow:
{problem_description}

The code you give previously is as follow:
{previous_answer}
    
The feedback is as follow:
{feedback}

The output format is a JSON structure followed by refined code:
{{
    'is_caused_by_you': false,
    'reason': 'leave empty string if the problem is not caused by you',
    'refined_code': 'Your refined code...'
}}
'''

    def __init__(self, model):
        super().__init__(
            name='Parameter Extractor',
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
        self.previous_answer = output
        return output

    def backward(self, feedback_pool):
        if not hasattr(self, 'problem'):
            raise NotImplementedError('Please call foward first!')
        output = self.backward_chain.predict(
            problem_description=self.problem['description'], 
            previous_answer=self.previous_answer,
            feedback=feedback_pool.get_current_comment_text())
        return output
