# Substrate examples

## Getting started

Get your API key from the [Substrate Dashboard](https://substrate/dashboard), and set it as an environment variable:

```bash
export SUBSTRATE_API_KEY=ENTER_YOUR_KEY
```

To run the Python examples, first install dependencies in the root directory.

```bash
poetry install --no-root
```

## Run examples

First, navigate to an example directory for your language. Then run:

```bash
# Run a TypeScript example
npm install                     # Install dependencies
npm start                       # Run example.ts

# Run a Python example
poetry run python example.py    # Run example.py
```
