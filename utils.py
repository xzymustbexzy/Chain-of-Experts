import ast
import re
import json
import os


def extract_code_from_string(input_string):
    # Match code within ```python ... ``` or ``` ... ``` blocks
    pattern = r'```(?:python)?\s*(.*?)\s*```'
    
    # Find all matches in the input string
    code_blocks = re.findall(pattern, input_string, re.DOTALL)

    if len(code_blocks) == 0:
        # print(f'Parse code error! {input_string}')
        return input_string
    elif len(code_blocks) == 1:
        return code_blocks[0]

    code_blocks = [code for code in code_blocks if 'pip' not in code]
    return '\n'.join(code_blocks)


def _extract_first_json_blob(text):
    starts = [i for i, c in enumerate(text) if c in ['{', '[']]
    for start in starts:
        stack = []
        quote_char = None
        escaped = False
        for idx in range(start, len(text)):
            ch = text[idx]
            if quote_char is not None:
                if escaped:
                    escaped = False
                    continue
                if ch == '\\':
                    escaped = True
                    continue
                if ch == quote_char:
                    quote_char = None
                continue

            if ch in ['"', "'"]:
                quote_char = ch
            elif ch in ['{', '[']:
                stack.append(ch)
            elif ch in ['}', ']']:
                if not stack:
                    break
                left = stack.pop()
                if (left == '{' and ch != '}') or (left == '[' and ch != ']'):
                    break
                if not stack:
                    return text[start:idx + 1]
    return None


def parse_json_from_string(text, expected_type=None):
    if text is None:
        raise ValueError('Input text is None')

    raw = str(text).strip()
    candidates = []
    if raw:
        candidates.append(raw)

    code = extract_code_from_string(raw).strip()
    if code and code not in candidates:
        candidates.append(code)

    blob = _extract_first_json_blob(raw)
    if blob and blob not in candidates:
        candidates.append(blob)
    blob = _extract_first_json_blob(code)
    if blob and blob not in candidates:
        candidates.append(blob)

    for candidate in candidates:
        for parser in (json.loads, ast.literal_eval):
            try:
                value = parser(candidate)
            except (ValueError, SyntaxError, json.JSONDecodeError):
                continue
            if expected_type is not None and not isinstance(value, expected_type):
                continue
            return value

    raise ValueError(f'Cannot parse JSON from text: {raw[:200]}')


def read_problem(dataset, problem_name):
    base_dir = 'dataset'
    with open(os.path.join(base_dir, dataset, problem_name, 'description.txt'), 'r', encoding='utf8') as f:
        description = f.read()

    with open(os.path.join(base_dir, dataset, problem_name, 'code_example.py'), 'r', encoding='utf8') as f:
        code_example = f.read()

    return {
        'description': description,
        'code_example': code_example
    }
