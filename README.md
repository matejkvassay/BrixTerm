# BrixTerm by LLMBrix

## About

Simple terminal app with OpenAI GPT assistance built in.

- automatically suggests fixes in unix commands if failed
- generates Python code in terminal and copies it into clipboard
- enables chat with GPT directly in terminal

## Usage guide

### Install

```bash
pip install brix-term
```

### Configure

```bash
# Configure OpenAI API access
export OPENAI_API_KEY='<TOKEN>'

# (optional) GPT model to be used, default is `gpt-4o-mini`
export BRIXTERM_MODEL='gpt-4o'

# (ALTERNATIVELY) API access for Azure AI is also supported
export AZURE_OPENAI_API_KEY='<TOKEN>'
export AZURE_OPENAI_API_VERSION='<VERSION>'
export AZURE_OPENAI_ENDPOINT='<ENDPOINT>'
```

### Run

```bash
brixterm
```
