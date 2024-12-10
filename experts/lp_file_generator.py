from experts.base_expert import BaseExpert

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI


class LPFileGenerator(BaseExpert):

    ROLE_DESCRIPTION = 'You are an LP file generator that expertises in generating LP (Linear Programming) files that can be used by optimization solvers.'
    FORWARD_TASK = '''As an LP file generation expert, your role is to generate LP (Linear Programming) files based on the formulated optimization problem. 

LP files are commonly used by optimization solvers to find the optimal solution. 
Here is the important part source from LP file format document: {knowledge}. 

Your expertise in generating these files will help ensure compatibility and efficiency. 
Please review the problem description and the extracted information and provide the generated LP file: 
{problem_description}.

The comments given by your colleagues are as follows: 
{comments}, please refer to them carefully.'''

    BACKWARD_TASK = '''When you are solving a problem, you get a feedback from the external environment. You need to judge whether this is a problem caused by you or by other experts (other experts have given some results before you). If it is your problem, you need to give Come up with solutions and refined code.

The original problem is as follow:
{problem_description}

The feedback is as follow:
{feedback}

The modeling you give previously is as follow:
{previous_modeling}

The output format is a JSON structure followed by refined code:
{{
    "is_caused_by_you": false,
    "reason": "leave empty string if the problem is not caused by you",
    "refined_result": "Your refined result"
}}
'''

    def __init__(self, model):
        super().__init__(
            name='LP File Generator',
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
        output = self.forward_chain.predict(
            problem_description=problem['description'], 
            comments_text=comments_text
        )
        self.previous_model = output
        return output

    def backward(self, feedback_pool):
        if not hasattr(self, 'problem'):
            raise NotImplementedError('Please call foward first!')
        output = self.backward_chain.predict(
            problem_description=self.problem['description'], 
            previous_answer=self.previous_answer,
            feedback=feedback_pool.get_current_comment_text())
        return output
