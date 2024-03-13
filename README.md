# Chain-of-Experts: When LLMs Meet Complex Operation Research Problems

## Requirements

1. Clone the repository
```bash
git clone https://github.com/dovedb/DoveDB_MVP.git
```

2. Install the necessary dependencies provided in the requirements.txt.
```bash
pip install -r requirements.txt
```

## Run

1. Download dataset
Download the LPWP and ComplexOR dataset.

2. Run the experiments
```bash
python run_exp.py --dataset LPWP --problem prob_0 --algorithm standard --model gpt-3.5.turbo-1106
```

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

