import random

from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI

from experts.base_expert import BaseExpert


class Conductor(BaseExpert):

    ROLE_DESCRIPTION='''you will take on the role of the conductor for a multi-expert system.'''
    FORWARD_TASK = '''Now, you are presented with an operational optimization-related problem: 
{problem_description}

In this multi-expert system, there are many experts, each of whom is responsible for solving part of the problem.
Your task is to CHOOSE THE NEXT EXPERT TO CONSULT.

The names of the experts and their capabilities are listed below:
{experts_info} 

Experts that have already been commented include: 
{commented_experts}

Please select an expert to consult from the remaining expert names {remaining_experts}.

Please note that the maximum number of asked experts is {max_collaborate_nums}, and you can ask {remaining_collaborate_nums} more times.

You should output the name of expert directly. The next expert is:'''

    def __init__(self, model):
        super().__init__(
            name='Conductor',
            description='An special expert that collaborates all other experts.',
            model=model
        )
        self.llm.max_tokens = 10

    def forward(self, problem, comment_pool, max_collaborate_nums):
        all_experts = comment_pool.all_experts
        all_experts_name = [e.name for e in all_experts]
        commented_experts_name = [c.expert.name for c in comment_pool.comments]

        experts_info = '\n'.join([str(e) for e in all_experts])
        commented_experts = str(commented_experts_name)     
        remaining_experts = str(list(set(all_experts_name) - set(commented_experts_name)))
        answer = self.forward_chain.predict(
            problem_description=problem['description'], 
            experts_info=experts_info,
            commented_experts=commented_experts,
            remaining_experts=remaining_experts,
            max_collaborate_nums=max_collaborate_nums,
            remaining_collaborate_nums=max_collaborate_nums-len(commented_experts),
        )
        expert_name_to_obj = { e.name: e for e in all_experts }
        for name, expert in expert_name_to_obj.items():
            if name in answer:
                return expert

        print('Can not find expert, random choice!')
        return random.choice(list(expert_name_to_obj.values()))

