import random

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI

from experts.base_expert import BaseExpert


class Conductor(BaseExpert):

    def __init__(self, model):
        super().__init__(
            name='Conductor',
            description='collaborate all experts',
            model=model
        )
        prompt_template = '''Now, you will take on the role of the conductor for a multi-expert system. 
Based on the capabilities of different experts and the current status of the problem-solving process, you need to decide which expert to consult next. 
You are presented with an operational optimization-related problem: {problem}
The current capabilities of the experts are as follows: {experts_info} 
Experts that have already been commented include: {commented_experts}
You should output the name of expert directly.'''
        llm = ChatOpenAI(
            model_name=self.model,
            temperature=0
        )
        self.llm_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate.from_template(prompt_template)
        )

    def forward(self, problem_description, workspace):
        
        experts_info = '\n'.join([str(e) for e in workspace.all_experts])
        commented_experts = ','.join([c.expert.name for c in workspace.comments])

        answer = self.llm_chain.predict(
            problem=problem_description, 
            experts_info=experts_info,
            commented_experts=commented_experts
        )

        expert_name_to_obj = { e.name: e for e in workspace.all_experts }
        for name, expert in expert_name_to_obj.items():
            if name in answer:
                return expert

        print('Can not find expert, random choice!')
        return random.choice(list(expert_name_to_obj.values()))

    def backward(self):
        pass
