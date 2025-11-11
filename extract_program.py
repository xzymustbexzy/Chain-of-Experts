import re
import os


def extract_code(text):
    """
    Extract Python code snippets from a given text.
    
    Args:
        text (str): The input text that may contain Python code snippets.
        
    Returns:
        list: A list of extracted Python code snippets.
    """
    # Define a regular expression pattern to match Python code blocks
    pattern = r'```python\n(.*?)\n```'
    
    # Find all code blocks in the text using the pattern
    code_blocks = re.findall(pattern, text, re.DOTALL)

    return '\n'.join(code_blocks)

# Example usage
for filename in os.listdir('gpt_result_generated_gt_program'):
    if not filename.endswith('.txt'):
        continue
    with open(os.path.join('gpt_result_generated_gt_program', filename), 'r') as f:
        text = f.read()
    code = extract_code(text)
    with open(os.path.join('gt_programs', filename[:-4] + '.py'), 'w') as f:
        f.write(code)
