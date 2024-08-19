# Title

<details>
    <summary>How to run this example</summary>

```bash
# Set your API key as an environment variable.
export SUBSTRATE_API_KEY=ENTER_YOUR_KEY

# Run the TypeScript example
cd typescript                   # Navigate to the typescript example
npm install                     # Install dependencies
ts-node example.ts              # Run the example

# Run the Python example
# Note: First install dependencies in the root examples directory.
cd python                       # Navigate to the python example
poetry run python example.py    # Run the example
```

</details>

![hero](hero.png)

To generate text with an LLM, use [`ComputeText`](https://www.substrate.run/nodes#ComputeText).

In the code snippets below, note how we've simplified the example code to:

- Use a hardcoded API key, rather than reading from an environment variable.
- Remove the main function
- Combine getting the result of a node and printing it

Try your best to limit extraneous content in both text and code.

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

When you're done, generate some images. You'll need a banner image.

- For the text, keep it simple, e.g. you can just use the name of a node: `ComputeText`.

```bash
cd _internal
poetry run marimo edit marketing.py
```

If your example is a graph, create a diagram. To edit the diagram, run:

```bash
d2 -w diagram.d2 diagram.svg
```
