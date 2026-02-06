from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from utils import extract_code_from_string


def solve(problem, model_name='gpt-3.5-turbo'):
    prompt_template = """You are a Python programmer in the field of operations research and optimization. Your proficiency in utilizing third-party libraries such as Gurobi is essential. In addition to your expertise in Gurobi, it would be great if you could also provide some background in related libraries or tools, like NumPy, SciPy, or PuLP.
You are given a specific problem. You aim to develop an efficient Python program that addresses the given problem.
Now the origin problem is as follow:\n{problem}\nGive your Python code directly."""
    llm = ChatOpenAI(
        model_name=model_name,
        temperature=0
    )
    llm_chain = PromptTemplate.from_template(prompt_template) | llm
    answer = llm_chain.invoke({'problem': problem})
    if hasattr(answer, 'content'):
        answer = answer.content
    else:
        answer = str(answer)
    code = extract_code_from_string(answer)
    return code
