# Substrate GenerateText Examples

To run this example,

```bash
# Set your API key as an environment variable.
# Get one here https://www.substrate.run/dashboard/keys if this is your first time.
export SUBSTRATE_API_KEY=<your Substrate API key>

# Navigate to the python example directory.
cd python
```

To run the example with Poetry, uncomment the Poetry sections in `pyproject.toml` and run the following.

```bash
poetry install
poetry run example
poetry run example-multi
```

To run the example with Rye, uncomment the Rye sections in `pyproject.toml` and run the following.

```bash
rye sync
rye run example
rye run example-multi
```
