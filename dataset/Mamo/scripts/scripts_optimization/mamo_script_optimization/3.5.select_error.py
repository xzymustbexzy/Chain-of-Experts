import json
import math
import argparse
from pathlib import Path
from tqdm import tqdm
from coptpy import *
import logging
import os
import random
import json
import shutil   

prompt = """
You are experienced engineer in optimization, please fix the errors to make sure the code can run successfully.
If there is no error, please return the original code.
And please do not change the original logic of the lp file. Your response should be entirely in .lp format, formatted to run directly without modifications.
Take a deep breathe before answering the question. This is a piece of cake to you.
PLEASE do not response anything except the code, No comments are allowed.

The followings are forbidden:
'''
This is the correct .lp file:
```lp
```
'''

Please avoid resposing above sentences.
Please output only the corrected code, with no additional text or explanations.
Here comes the lp:
{lp_code}
Generate the correct .lp format, starting with the objective function and followed by the constraints, without any additional sentences. The constraints should be formatted as 'variable + variable >= number' for inequalities, all the variables shoule on the left hand side of the inequality . Ensure there is a space between variables and their coefficients (coefficients should be numerical).
The correct lp code is:
"""


error_code = []
query = []
prompts = []
def generate_query(code):
    chatgpt_query = prompt
    # print(data)
    chatgpt_query = chatgpt_query.format_map({'lp_code': f'{code}'})
    return chatgpt_query


def read_jsonl_file( error_dir):
    error_id = []
    code = []
    error = []
    error_dir = Path(error_dir)
    for item in tqdm(error_dir.glob("*.lp"), desc="Processing error files"):
        # output = solver(item)
        file_id = int(item.stem.split('_')[-1])
        error_id.append(file_id)
        with open(item, 'r', encoding='utf-8') as code_file:
            code_content = code_file.read()
            code.append(code_content)

    return code, error_id

def write_response(content, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Failed to write file {output_path}: {e}")

def process_data(error_dir, output_dir):
    code,  ids = read_jsonl_file(error_dir)
    # 39/ 346
    for i in tqdm(range(len(ids)), desc="Processing data"):
        prompts.append(generate_query(code[i]))
        # response = model.call(generate_query(code[i]))
        query.append({
            'id': ids[i],
            'query': prompts[i]
        })

    output_path = output_dir / f"lp_errors_query.jsonl"
    with open(output_path, 'w', encoding='utf-8') as file:
        for item in query:
            file.write(json.dumps(item) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process data using OpenAI models.")
    parser.add_argument('-e', '--error_dir', type=str, help="Error directiory.")
    parser.add_argument('-o', '--output_dir', type=str, help="Output directory for corrected py files.")
    
    args = parser.parse_args()
    
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    process_data(args.error_dir, output_dir)
