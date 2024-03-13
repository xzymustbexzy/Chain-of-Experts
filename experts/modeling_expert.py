from experts.base_expert import BaseExpert

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI


prompt_template = '''You are a modeling expert specialized in the field of Operations Research and Optimization. Your expertise lies in Mixed-Integer Programming (MIP) models, and you possess an in-depth understanding of various modeling techniques within the realm of operations research. At present, you are given an Operations Research problem, alongside additional insights provided by other experts. The goal is to holistically incorporate these inputs and devise a comprehensive model that addresses the given production challenge.
Now the origin problem is as follow:
{problem}
And the comments from other experts are as follow:
{comments_text}

Give your model of this problem.'''


class ModelingExpert(BaseExpert):

    def __init__(self, model):
        super().__init__(
            name='Modeling Expert',
            description='Proficient in constructing mathematical optimization models based on the extracted information.',
            model=model  
        )
        self.prompt_template = prompt_template

        llm = ChatOpenAI(
            model_name=model,
            temperature=0
        )
        self.llm_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate.from_template(self.prompt_template)
        )

    def forward(self, problem, comment_pool):
        comments_text = comment_pool.get_current_comment_text()
        print('-' * 30)
        print('Input of modeling expert:')
        print(prompt_template.format(problem=problem['description'], comments_text=comments_text))
        output = self.llm_chain.predict(problem=problem['description'], comments_text=comments_text)
        print()
        print('Output of modeling expert:')
        print(output)
        print()
        return output

    def backward(self):
        pass
