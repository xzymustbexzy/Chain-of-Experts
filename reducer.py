from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI

from experts.base_expert import BaseExpert


class Reducer(BaseExpert):

    ROLE_DESCRIPTION = 'You are an expert that responsible for summarize the comment of all other experts then conclude the final answer'
    FORWARD_TASK = '''Now, you are an expert of Operations Research.
You are supposed to give the final code of an problem.
Text description of the problem: {problem_description}
Your colleagues are all experts in various related fields. They have given their own insights. I hope you will carefully refer to these comments when giving the final code:
{comment_text}

No code is required outside the function except for the import package (No test code).
Your final code is as following:
'''

    def __init__(self, model):
        super().__init__(
            name='Solver',
            description='Reduce all comments given by other experts',
            model=model
        )

    def forward(self, problem_description, workspace):
        comment_text = workspace.get_current_comment_text()
        answer = self.forward_chain.predict(
            problem_description=problem_description, 
            comment_text=comment_text
        )
        return answer

