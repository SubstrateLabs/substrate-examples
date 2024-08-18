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

...Intro in a few sentences...

...Walk through the code...

```python Python
# example.py
import os
from substrate import Substrate, ComputeText

def main():
    api_key = os.environ.get("SUBSTRATE_API_KEY") or "YOUR_API_KEY"
    substrate = Substrate(api_key=api_key)

    story = ComputeText(prompt="tell me a short 2-sentence story")
    response = substrate.run(story)

    story_out = response.get(story)
    print(story_out.text)
```

```typescript TypeScript
// example.ts
import { Substrate, ComputeText } from "substrate";

async function main() {
  const apiKey = process.env["SUBSTRATE_API_KEY"] || "YOUR_API_KEY";
  const substrate = new Substrate({ apiKey: apiKey });

  const story = new ComputeText({ prompt: "tell me a short 2-sentence story" });
  const res = await substrate.run(story);

  const summaryOut = res.get(story);
  console.log(summaryOut.text);
}
```

...Recap in a few sentences ....

## See also

- ...Related Substrate posts...
- ...Substrate node documentation...
