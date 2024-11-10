# pipefy-tools

A simple Python library to interact with the Pipefy API, currently  in the early stages of development.

## 🚧 Work in Progress

Some features might be incomplete or in early stages of development. Contributions, suggestions, and issue reports are welcome!

### Current Features:

#### Queries
- Get table record fields
- Get table record ID

#### Mutations
- Set table record field value

<!-- ### To Do: -->

## How to Use

### Requirements

- Python 3.x
- `requests` library

### Installation

To install the required dependencies, run the following command:

```bash
pip install requests
```

### Configuration

Before using the project, you need to configure your token. Follow the steps below:
- Generate your token via the link https://app.pipefy.com/tokens
- Open the file `pipefy-token.py`
- Place the token in the variable `personal_access_token`

Now, run the code provided in `main.py` file to check if your token is set up correctly.

### Usage [WIP]
`main.py` code:
```python
import pipefy_api as pipe

response = pipe.me()

if response.status_code == 200:
    print("API communication was successful!\n"
          f"API Response: {response.text}")
else:
    print("There was an error communicating with the API.\n"
          f"Response status code: {response.status_code}\n"
          f"Details: {response.text}")
```
