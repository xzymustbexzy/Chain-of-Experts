import subprocess
import sys
import math
import json
import argparse
from tqdm import tqdm
import logging
from pathlib import Path
import shutil



def main(args):
    data_folder = Path(args.data_folder)
    for item in tqdm(data_folder.glob("*.py"), desc="Fixing synatix error"):
        with open(item, 'r', encoding='utf-8') as f:
            data = f.read()
            data = data.replace('```python', '').replace('```', '').replace(" from", "from")
        with open(item, 'w', encoding='utf-8') as f:
            f.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process and compare python files.")
    parser.add_argument('--data_folder', type=str, required=True, help="Path to the folder containing python files.")
    
    args = parser.parse_args()
    main(args)