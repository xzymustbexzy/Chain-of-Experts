import random
import json
from pathlib import Path
import argparse
from tqdm import tqdm
import os

prompt = """
You are experienced python engineer, the following codes may have some errors (in syntax), with the error information {error_info}, please fix the errors to make sure the code can run successfully.
If there is no error, please return the original code.
And please do not change the original logic of the code. Your response should be entirely in Python code, formatted to run directly without modifications.
Take a deep breathe before answering the question. This is a piece of cake to you.
PLEASE do not response anything except the code, No other comments outside the code are allowed.

The followings are forbidden:
'''
The code is almost correct, but there is a syntax error in the function `round_to_significant_figures`. The round function is missing a closing parenthesis. Here is the corrected version:

```python
```
'''

Please avoid resposing above sentences.
Please output only the corrected code, with no additional text or explanations.
Here comes the code:
{code}

The correct code is:
"""


error_code = []
prompts = []
query = []
def generate_query(code, error):
    chatgpt_query = prompt
    # print(data)
    chatgpt_query = chatgpt_query.format_map({'code': f'{code}', 'error_info': f'{error}'})
    return chatgpt_query

def read_jsonl_file(file_path, error_dir):
    error_id = []
    code = []
    error = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            current = json.loads(line)
            error.append(current['error'])
            error_id.append(current['id'])
    for ids in error_id:
        code_path = os.path.join(error_dir, f"ode_code_{ids}.py")
        with open(code_path, 'r', encoding='utf-8') as code_file:
            code_content = code_file.read()
            code.append(code_content)
    return code, error, error_id

def write_response(content, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Failed to write file {output_path}: {e}")

def process_data(error_dir, file_path, output_dir):
    code, error, ids = read_jsonl_file(file_path, error_dir)
    for i in tqdm(range(len(ids)), desc="Processing data"):
        prompts.append(generate_query(code[i], error[i]))
        query.append({
            'id': ids[i],
            'query': prompts[i]
        })
    output_path = output_dir / f"ode_errors_query.jsonl"
    with open(output_path, 'w', encoding='utf-8') as file:
        for item in query:
            file.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process data using OpenAI models.")
    parser.add_argument('-e', '--error_dir', type=str, help="Error directiory.")
    parser.add_argument('-f', '--file_path', type=str, help="File path containing error info.")
    parser.add_argument('-o', '--output_dir', type=str, help="Output directory for corrected py files.")
    
    args = parser.parse_args()
    
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    process_data(args.error_dir, args.file_path, output_dir)
