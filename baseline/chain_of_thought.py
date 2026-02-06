from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from utils import extract_code_from_string


def solve(problem_data, model_name='gpt-3.5-turbo'):
    problem_description = problem_data['description']
    code_example = problem_data['code_example']
    prompt_template = """You are a Python programmer in the field of operations research and optimization. Your proficiency in utilizing third-party libraries such as Gurobi is essential. In addition to your expertise in Gurobi, it would be great if you could also provide some background in related libraries or tools, like NumPy, SciPy, or PuLP.
You are given a specific problem. You aim to develop an efficient Python program that addresses the given problem.
Now the origin problem is as follow:
{problem_description}
Let's analyse the problem step by step, and then give your Python code.
Here is a starter code:
{code_example}"""

    llm = ChatOpenAI(
        model_name=model_name,
        temperature=0
    )
    llm_chain = PromptTemplate.from_template(prompt_template) | llm
    answer = llm_chain.invoke({'problem_description': problem_description, 'code_example': code_example})
    if hasattr(answer, 'content'):
        answer = answer.content
    else:
        answer = str(answer)
    return answer
