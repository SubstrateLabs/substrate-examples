# Substrate examples

Substrate [Python](https://github.com/SubstrateLabs/substrate-python) and [TypeScript](https://github.com/SubstrateLabs/substrate-typescript) examples.

- [Basics](/basics) – Get started with basic examples.
- [Techniques](/techniques) – Prompting techniques (Tree of Thought, Mixture of Agents), RAG techniques, and more.
- [Tutorials](/tutorials) – Integrated use cases, like multi-turn conversations (chat).

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
# Note: First install dependencies in the root directory (see above).
poetry run python example.py    # Run example.py
```
