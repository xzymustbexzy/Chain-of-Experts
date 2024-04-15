# Chain-of-Experts: When LLMs Meet Complex Operation Research Problems

## Requirements

1. Clone the repository
```bash
git clone https://github.com/xzymustbexzy/Chain-of-Experts.git
```

2. Install the necessary dependencies provided in the requirements.txt.
```bash
pip install -r requirements.txt
```

## Run the experiments
Firstly, set the environment variable `OPENAI_API_KEY`

```bash
export OPENAI_API_KEY=[Your API key here]
```

Run the experimental script

```bash
python run_exp.py --dataset LPWP --problem "prob_.*" --algorithm coe
```

## Usage
- `--dataset`: Specifies the dataset name. Currently supports "LPWP" or "ComplexOR". This argument is required.

- `--problem`: Specifies the name of the problem to solve. This argument is required.

- `--algorithm`: Specifies the algorithm to use. Supported algorithms include 'standard', 'chain_of_thought' ('cot'), 'progressive_hint' ('php'), 'solo_performance_prompting' ('ssp'), and 'reflexion'. This argument is required.

- `--enable_reflection`: Adds reflection capabilities to the selected algorithm. This is optional and is disabled by default.
- `--log_dir`: Specifies the directory where logs will be stored. The default is 'log'.
- `--model`: Specifies the base large language model to use. The default is 'gpt-3.5-turbo'.
- `--max_collaborate_nums`: Sets the maximum number of collaborations allowed. The default value is 3.
- `--max_trials`: Sets the maximum number of forward-backward trials allowed. The default value is 3.

## Dataset
The LPWP dataset is uploaded in this repo.

Please note that the ComplexOR dataset is still in the review stage, and we have uploaded a raw version of the ComplexOR dataset. The formal 37 datasets mentioned in the paper will be released soon.

## Citation
```
@inproceedings{
xiao2024chainofexperts,
title={Chain-of-Experts: When {LLM}s Meet Complex Operations Research Problems},
author={Ziyang Xiao and Dongxiang Zhang and Yangjun Wu and Lilin Xu and Yuan Jessica Wang and Xiongwei Han and Xiaojin Fu and Tao Zhong and Jia Zeng and Mingli Song and Gang Chen},
booktitle={The Twelfth International Conference on Learning Representations},
year={2024},
url={https://openreview.net/forum?id=HobyL1B9CZ}
}
```

