# Tree of Thought

<details>
<summary>How to run this example</summary>
<br/>

```bash
# Set your API key as an environment variable.
export SUBSTRATE_API_KEY=ENTER_YOUR_KEY

# Run the TypeScript example

# If using tsx:
cd typescript                   # Navigate to the typescript example
npm install                     # Install dependencies
npx tsx example.ts              # Run the example

# If using Deno:
cd typescript
deno run example.ts

# Run the Python example

# If using Poetry:
cd python                       # Navigate to the python example
poetry install                  # Install dependencies and build the example
poetry run main                 # Run the example

# If using Rye:
# Update pyproject.toml to switch to Rye.
cd python
rye sync
rye run main
```

</details>

![hero](hero.jpg)

## Overview

Tree of Thought (ToT) is an advanced prompting technique for large language models (LLMs) that enhances problem-solving capabilities by simulating a multi-step reasoning process. This approach encourages the model to:

1. Break down complex problems into smaller, manageable sub-problems
2. Generate multiple potential solutions or "thoughts" for each sub-problem
3. Evaluate and prune less promising paths
4. Combine the most promising thoughts to form a coherent solution

By mimicking human-like reasoning, ToT allows LLMs to tackle more challenging tasks, improve accuracy, and provide more transparent decision-making processes. This technique is particularly useful for problems requiring multi-step reasoning, strategic planning, or creative problem-solving.

There are a few novel problems which can be solved using this technique, like solving a Sudoku puzzle, but it seems equally suited to improving LLM responses by providing a structured and transparent reasoning process.  Our example asks the model to reason through a game of Hide and Seek, displaying the final reasoning behind where the LLM believes the hider to be. 

While putting this example together, we found that the general structure can be remain while changing only the initial framing of the problem, with interesting results coming from simply changing prompt text.  Try asking it to refine a short story in a specific style or to play a different kind of game!

## How it works

In our example, the tree is represented by a panel of experts at each step - we prompt the LLM for multiple responses to a given prompt, and then ask it to rank those responses and choose the best one.  This can be thought of as a breadth-first approach to tree pruning, since we explore each of the next paths before moving to the next layer.  This is in contrast to a depth-first approach, where we explore each path to its end before moving to the next.

The key to this process is the repeated process of generating multiple alternative responses to a prompt followed by synthesis of those responses.  This feedback loop allows the LLM to refine its reasoning and improve its output over time.

![diagram](diagram.svg)
