# BrixTerm

## About

**BrixTerm** is a simple terminal app that integrates GPT to assist with everyday development tasks.

---

## Features

- Automatically suggests fixes for failed Unix commands
- Generates Python code and copies it directly to your clipboard
- Built-in chatbot accessible inside the terminal

> **Note:** This tool is **not fully agentic** — developers maintain control by using pre-defined commands.

---

## Available Commands

### 1. TERMINAL (default)

Type any terminal command.
If it fails, the AI will suggest a corrected version.

---

### 2. INTERACTIVE SHELL

Use `!<command>` to run an interactive shell command.
Without the `!`, interactive commands timeout after 10 seconds.
**Example:** `!htop`

---

### 3. CODE GEN

Use `c <your request>` to generate Python code.
The result is automatically copied to your clipboard.

---

### 4. CODE GEN + CLIPBOARD

Use `ccc <your request>` to generate Python code.
The content of your clipboard is passed to the AI as context.
The result is copied back to your clipboard.

---

### 5. ANSWER

Use `a <your request>` to chat with GPT.

---

### 6. EXIT

Use `q` to exit the application.
_____________________________________________________________________
Powered by *LLMBrix* library: https://github.com/matejkvassay/LLMBrix

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

# (optional) Optimize colors for light mode (dark is default)
export BRIXTERM_COLOR_MODE='light'

# (ALTERNATIVELY) API access for Azure AI is also supported
export AZURE_OPENAI_API_KEY='<TOKEN>'
export AZURE_OPENAI_API_VERSION='<VERSION>'
export AZURE_OPENAI_ENDPOINT='<ENDPOINT>'
```

### Run

```bash
brixterm
```

### Run options

(env vars have priority over these)

```bash
brixterm --help
usage: brixterm [-h] [--dev] [--light_mode] [--model MODEL]

BrixTerm AI Terminal

options:
  -h, --help     show this help message and exit
  --dev          (optional) Run in development mode with Arize Phoenix tracing enabled.
  --light_mode   (optional) Optimize looks for light mode terminal (dark is default).
  --model MODEL  (optional) Specify GPT model. (default='gpt-4o-mini')
```
