# GenAI API Tester Blocks

This repository contains various Python scripts to test and interact with APIs using different tools and libraries. The main focus is on generating test cases and executing them using LangChain, OpenAI, and other related libraries.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/anupmanekar/genai-api-tester-blocks.git
   cd genai-api-tester-blocks
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

To run any of the scripts, simply execute them using Python. For example:
```bash
python 01_test_code_by_instruct.py
```

## Examples of Usage and Expected Output

### Example 1: Generating Python Testing Code for REST API
```bash
python 01_test_code_by_instruct.py
```
Expected output:
```python
# Generated Python code for testing the REST API
```

### Example 2: Using Python Tool to Execute Code
```bash
python 02_use_python_tool_execute_code.py
```
Expected output:
```python
hello
```

## Dependencies

The project relies on the following main dependencies:
- `langchain`
- `openai`
- `faiss-cpu`
- `tiktoken`
- `requests`
- `pytest`

To install all dependencies, run:
```bash
pip install -r requirements.txt
```
