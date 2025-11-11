# <span style="color:blue"><b>Mamo</b></span>: a <span style="color:blue"><b>Ma</b></span>thematical <span style="color:blue"><b>Mo</b></span>deling Benchmark with Solvers

<!-- <p align="center">
  <a 📃 href="https://arxiv.org/abs/2405.13144">Our Paper</a>
</p> -->


## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
  - [Data Description](#data-description)
  - [Running Benchmark](#running-benchmark)
<!-- - [Results](#results)
- [Citation](#citation) -->

## Introduction
Wellcome to Mamo! This is a benchmark for mathematical modeling. 



## Installation

### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed [Git](https://git-scm.com/).
- You have a [GitHub](https://github.com/) account.
- You have access to the terminal (Command Prompt on Windows, Terminal on macOS and Linux).
- If you want to run Optimization parts, please make sure you have an optimization solver that can read .lp file installed (Here we use COPT, you could use the solver you want and do some small change in the codes)

### Clone the Repository
To get started, clone the repository and install the necessary dependencies:
```bash
cd ~/Projects
git clone https://github.com/FreedomIntelligence/Mamo.git
cd Mamo
```

- For the close source models, we call the APIs, the requirements are:
```bash
pip install -r requirements.txt
```

- For open source models, we use VLLM for deployment and inference.
```bash
pip install vllm
```

Replace the ~/Projects with the directionary for Mamo


## Usage
  ### data-description
  - The data consists of two parts: ODE and Optimization, while optimziation part consists of Easy_LP and Complex_LP, see in Data folder (mamo_ode.jsonl, mamo_complex_lp.jsonl, mamo_easy_lp.jsonl)
  - Each data is a json object, with 
  ```json
  {
      "id": id, 
      "Question": the question, 
      "Answer": the answer, 
      "Category": ode/optimization, 
      "Type": first_order_equation/.../easy_lp/complex_lp
  }
  ```
  ### Running Benchmark

  To run the benchmark(for close source model calling API), follow these steps:

  1. **Navigate to the Script Directory**:
  First, go to the appropriate script directory. Depending on your needs, use one of the following commands:
  ```bash
  cd scripts/scripts_optimization/mamo_script_optimization
  or 
  cd scripts/scripts_ode/mamo_script_ode
  ```

  2. **Fill in the Required Paths**
    Ensure all necessary path variables are correctly set in your environment or script files.

  3. **Execute the Scripts in Bash**:
  Run the following scripts in order. Choose the appropriate set of scripts based on whether you are working with ODE or optimization:

  - For ODE
  ```bash
  bash 1.prepare_query_ode.sh
  bash 2.run_model_ode.sh
  bash 3.run_code_comp_ode.sh
  bash 4.fix_error_ode.sh
  bash 5.rerun_code_comp_ode.sh
  ```

  - For Optimization:
  ```bash
  bash 1.prepare_query_optimization.sh
  bash 2.run_model_optimization.sh
  bash 3.run_code_comp_optimization.sh
  bash 4.fix_error_optimization.sh
  bash 5.rerun_code_comp_optimization.sh
  ```

  To run the benchmark(for open source model), follow these steps:

  1. **Navigate to the Script Directory**:
  First, go to the appropriate script directory. Depending on your needs, use one of the following commands:
  ```bash
  cd scripts/scripts_optimization/mamo_script_optimization
  or 
  cd scripts/scripts_ode/mamo_script_ode
  ```

  2. **Fill in the Required Paths**
    Ensure all necessary path variables are correctly set in your environment or script files.

  3. **Execute the Scripts in Bash**:
  Run the following scripts in order. Choose the appropriate set of scripts based on whether you are working with ODE or optimization:

  - For ODE
  ```bash
  bash 1.prepare_query_ode.sh
  bash 2.run_model_ode_open.sh
  bash 3.run_code_comp_ode.sh
  bash 4.fix_error_ode_open.sh
  bash 5.rerun_code_comp_ode.sh
  ```

  - For Optimization:
  ```bash
  bash 1.prepare_query_optimization.sh
  bash 2.run_model_optimization_open.sh
  bash 3.run_code_comp_optimization.sh
  bash 4.fix_error_optimization_open.sh
  bash 5.rerun_code_comp_optimization.sh
  ```

  ### Few-shot Experiment

  To run the few shots experiment, here is the instruction:

  1. **Navigate to the Script Directory**:
  Select the target file based on your needs and use one of
  ```bash
  cd scripts/scripts_optimization/few_shot_scripts_ode
  cd scripts/scripts_ode/few_shot_scripts_optimization
  ```
  2. **Fill in the Required Paths**:
  Make sure to update file paths and adjust environment-specific parameters in the scripts in your local environment.

  3. **Select data from datasets**:
  Extract samples from the corresponding data sets (`mamo_ode.jsonl`, `mamo_complex_lp.jsonl`, `mamo_easy_lp.jsonl`) to form the data sets (`ode_select.jsonl`, `lp_select.jsonl`) of few shots.

  4. **Update the appropriate prompts**:
  Choose the prompts with the number of shots you need from data folders `ode_few_shot_prompt` and `lp_few_shot_prompt` to update the `prompt_template`" in the `1.prepare_query_ode.py` and `1.prepare_query_optimization.py` respectively.

  5. **Execute the Scripts in Bash**:
  Adopt the scripts sequentially depending on your needs as listed below.
  - For ODE
  ```bash
  bash 1.prepare_query_ode.sh
  bash 2.run_model_ode.sh
  bash 3.run_code_comp_ode.sh
  bash fix_error_ode.sh
  ```

  - For Optimization:
  ```bash
  bash 1.prepare_query_optimization.sh
  bash 2.run_model_optimization.sh
  bash 3.run_code_comp_optimization.sh
  call remove_quotes.bat
  ```



## Result


 ## Citation

If you use this work, please cite it as follows:

```bibtex
@misc{huang2024mamo,
      title={Mamo: a Mathematical Modeling Benchmark with Solvers}, 
      author={Xuhan Huang and Qingning Shen and Yan Hu and Anningzhe Gao and Benyou Wang},
      year={2024},
      eprint={2405.13144},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```
