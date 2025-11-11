import json
import math
import argparse
from pathlib import Path
from tqdm import tqdm
from coptpy import *
import logging
import os
import openai
import random
import json
import shutil   

openai.api_base = ""

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
def generate_query(code):
    chatgpt_query = prompt
    # print(data)
    chatgpt_query = chatgpt_query.format_map({'lp_code': f'{code}'})
    return chatgpt_query

class OpenAIModel:
    def __init__(self, model_name, keys_path):
        self.model_name = model_name
        with open(keys_path, encoding="utf-8") as fr:
            self.keys = [line.strip() for line in fr if len(line.strip()) >= 4]

    def call(self, message, temp = 0.8):
        try:
            current_key = random.choice(self.keys)
            openai.api_key = current_key
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": message}],
                temperature=temp
            )
            return response
        except Exception as e:
            print(f"API call failed: {e}")
            return None

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

def process_data(error_dir, output_dir, model):
    code,  ids = read_jsonl_file(error_dir)
    # 39/ 346
    for i in tqdm(range(len(ids)), desc="Processing data"):
        response = model.call(generate_query(code[i]))
        if response:
            content = response['choices'][0]['message']['content']
            output_path = output_dir / f"lp_model_{ids[i]}.lp"
            write_response(content, output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process data using OpenAI models.")
    parser.add_argument('-e', '--error_dir', type=str, help="Error directiory.")
    parser.add_argument('-o', '--output_dir', type=str, help="Output directory for corrected py files.")
    parser.add_argument('-k', '--keys_path', type=str, help="File path containing API keys.")
    parser.add_argument('-m', '--model_name', type=str, default="gpt-4", help="OpenAI model name.")
    parser.add_argument('--temperature', type=float, default=0.8, help="Response temperature.")
    
    args = parser.parse_args()
    
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    model = OpenAIModel(model_name=args.model_name, keys_path=args.keys_path)
    process_data(args.error_dir, output_dir, model)
