import os

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class PromptModelChain:
    def __init__(self, prompt, llm):
        self.chain = prompt | llm

    def predict(self, **kwargs):
        response = self.chain.invoke(kwargs)
        if hasattr(response, 'content'):
            return response.content
        return str(response)


class BaseExpert(object):

    def __init__(self, name, description, model):
        self.name = name
        self.description = description
        self.model = model

        llm_kwargs = {
            'model_name': model,
            'temperature': 0,
        }
        openai_api_base = os.getenv('OPENAI_API_BASE')
        if openai_api_base:
            llm_kwargs['openai_api_base'] = openai_api_base

        self.llm = ChatOpenAI(**llm_kwargs)
        self.forward_prompt_template = self.ROLE_DESCRIPTION + '\n' + self.FORWARD_TASK
        self.forward_chain = PromptModelChain(
            prompt=PromptTemplate.from_template(self.forward_prompt_template),
            llm=self.llm,
        )
        if hasattr(self, 'BACKWARD_TASK'):
            self.backward_prompt_template = self.ROLE_DESCRIPTION + '\n' + self.BACKWARD_TASK
            self.backward_chain = PromptModelChain(
                prompt=PromptTemplate.from_template(self.backward_prompt_template),
                llm=self.llm,
            )

    def forward(self):
        pass

    def backward(self):
        pass

    def __str__(self):
        return f'{self.name}: {self.description}'
