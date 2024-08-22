# Substrate Example Templates in Python

This is a Substrate example template written in Python. To run this example,

```bash
# Set your API key as an environment variable.
# Get one here https://www.substrate.run/dashboard/keys if this is your first time.
export SUBSTRATE_API_KEY=<your Substrate API key>

# Navigate to the python example directory.
cd python
```

To run the example with Poetry (default), run the following.

```bash
poetry install
poetry run main
```

To run the example with Rye, comment out the Poetry sections and uncomment the Rye sections in `pyproject.toml` and run the following.

```bash
rye sync
rye run main
```