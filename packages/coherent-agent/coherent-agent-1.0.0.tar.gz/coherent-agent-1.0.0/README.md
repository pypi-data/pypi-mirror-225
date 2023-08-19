# Agent Package

The Coherent-Agent package is a set of tools designed to make working with Large Language Models a breeze. Whether you're building or testing prompts, generating code, running interviews or analyzing text, we've got you covered!

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/coherent-api/agent.git
   ```

2. Create a virtual environment with Pyenv or Conda:

    ```bash
    pyenv virtualenv 3.10 agent-env
    ```

    ```bash
    conda create --name agent-env python=3.10 pip
    ```

3. Activate the environment:

    ```bash
    pyenv activate agent-env
    ```

    ```bash
    conda activate agent-env
    ```

4. Install the required python packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Navigate to tools and play around with common agent tasks:

    ```bash
    python tools/generate_prompt_from_user_input.py
    ```
