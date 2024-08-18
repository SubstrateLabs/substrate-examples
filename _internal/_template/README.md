# Title

## Running this example

```bash
# Set your API key as an environment variable.
export SUBSTRATE_API_KEY=ENTER_YOUR_KEY

# Run the TypeScript example
cd typescript                   # Navigate to the typescript example
npm install                     # Install dependencies
npm start                       # Run example.ts

# Run the Python example
# Note: First install dependencies in the root examples directory.
cd python                       # Navigate to the python example
poetry run python example.py    # Run example.py
```

# Walkthrough

This is a template that you can use as a starting point for a Substrate blog post or guide.

In the code snippets below, note how we've simplified the example code to:

- Use a hardcoded API key, rather than reading from an environment variable.
- Remove the main function
- Combine getting the result of a node and printing it

Try your best to simplify and limit extraneous content in example code.

```python Python
# example.py
from substrate import Substrate, ComputeText

substrate = Substrate(api_key="YOUR_API_KEY")

story = ComputeText(prompt="tell me a short 2-sentence story")
res = substrate.run(story)

print(res.get(story).text)
```

```typescript TypeScript
// example.ts
import { Substrate, ComputeText } from "substrate";

const substrate = new Substrate({ apiKey: "YOUR_API_KEY" });

const story = new ComputeText({ prompt: "tell me a short 2-sentence story" });
const res = await substrate.run(story);

console.log(res.get(story).text);
```

This is a basic example of using Substrate's `ComputeText` node to generate text using an LLM.
