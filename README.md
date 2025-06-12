# BrixTerm by LLMBrix

## About

AI powered terminal app for Python developers.

Has to be configured via ENV variables (see below).

Works with OpenAI models only.

## Features

- no command - either execute a terminal command. If command fails AI will suggest fix
- you can directly spell out commands in natural language
- type `a my question` for answer mode - chatbot in your terminal
- type `c my question` for code mode - terminal generates piece of Python code and copies it to clipboard
- chat history supported for all 3 modes (terminal, answer and code)
- support for interactive sessions (e.g. `htop`)
- history of commands (up to 1000 commands stored, retrieve with arrow up/down)
- completions with TAB

## Install

`pip install brix-term`

## Configure

Set following ENV variables:

```bash
# (OPTIONAL) Model to be used, default is gpt-4o-mini, can use 'gpt-4o'
export BRIX_TERM_MODEL='gpt-4o-mini'

# (OPTIONAL) How many conversation turns to store in chat history, defaults are 3, 5, 3, as shown
export TERM_MODE_HIST=3
export ANSWER_MODE_HIST=5
export CODE_MODE_HIST=3

# Configure LLM API for OpenAI
export OPENAI_API_KEY='<TOKEN>'

# (OR) Configure LLM API for Azure OpenAI
export AZURE_OPENAI_API_KEY='<TOKEN>'
export AZURE_OPENAI_API_VERSION='<VERSION>'
export AZURE_OPENAI_ENDPOINT='<ENDPOINT>'
```

## Run

Type in your terminal:

`brixterm`

## Use

- type valid unix command and it will run
- type command with typo `jit commit -am 'wip'`, it will fail. AI will automatically suggest fixed command
  version, confirm with `y`
- type natural language sentence not starting with unix keyword e.g. `list all files in this dir ending with .py`",
  confirm with `y`
- `a what is diameter of earth?` - will trigger answer mode, chatbot will answer in terminal directly
- `c deduplicate pandas dataframe` - code will be generated into terminal and copied to clipboard
- `e` or `q` to exit

## License

This project is licensed under the MIT License.

### Third-Party Licenses

This project includes open-source components licensed under their own terms.
See `THIRD_PARTY_LICENSES.txt` for details.
