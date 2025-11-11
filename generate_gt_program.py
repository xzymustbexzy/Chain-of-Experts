import os
import json
import requests
import time


API_KEY = 'sk-15xff33b700432d5d2d9c723f883326064b6f0a6ae6m4BsM'
base_url = 'api.gptsapi.net'


def call_gpt(
        question, 
        model, 
        temperature=1,
        max_tokens=None, 
        max_retries=3, 
        retry_delay=60):
    for attempt in range(max_retries):
        url = f'https://{base_url}/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer ' + API_KEY,
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": 'You are an helpful assistant'},
                {"role": "user", "content": question},
            ]
        }
        if max_tokens is not None:
            data['max_tokens'] = max_tokens

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            response = response.json()
            return response['choices'][0]['message']['content']
        except requests.RequestException as e:
            print('Request failed:', e)
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise


for problem_name in os.listdir('dataset/ComplexOR'):
    if not os.path.exists(os.path.join('dataset', 'ComplexOR', problem_name, 'gt_model.txt')):
        continue
    
    with open(os.path.join('dataset', 'ComplexOR', problem_name, 'description.txt'), 'r') as f:
        problem_description = f.read()

    with open(os.path.join('dataset', 'ComplexOR', problem_name, 'gt_model.txt'), 'r') as f:
        gt_model = f.read()

    with open(os.path.join('dataset', 'ComplexOR', problem_name, 'code_example.py'), 'r') as f:
        code_example = f.read()

    question = f'这是一个运筹优化问题：\n{problem_description}\n\n这是它对应的数学建模\n{gt_model}\n\n现在，有一段python代码，它仅仅是该问题对应的代码框架：\n{code_example}\n\n你是一位运筹优化领域的编程专家，请根据数学建模完成它的对应代码。'
    result = call_gpt(question, model='gpt-4')

    with open(f'gpt_result_generated_gt_program/{problem_name}.txt', 'w') as f:
        f.write(result)
    time.sleep(30)
