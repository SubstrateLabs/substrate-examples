# Skeleton of Thought

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

![hero](hero.png)

[Skeleton of Thought](https://www.prompthub.us/blog/reducing-latency-with-skeleton-of-thought-prompting) is a technique used to generate improved LLM content by first creating a skeleton containing
an outline of points to include and then generating content for each point before stitching the final content together.

This technique has been found to be expecially helpful for creating responses to "knowlege" oriented queries where a
better result depends on having clear responses for a set of supporting points. This technique is not a good fit for
cases that require sequential reasoning or planning however because the points are elaborated on in isolation.

Substrate can make implementing this idea relatively straight forward and because we can run many LLM calls in paralell 
it can be done performatly when generating responses for each individual point.

Let's walk through how we might set this up using both TypeScript and Python.

First we'll need to make sure we're importing the SDK object we need and initializing the Substrate API client.

In TypeScript it will look like this:

```typescript
import { ComputeText, ComputeJSON, Substrate, sb } from "substrate";
const apiKey = process.env["SUBSTRATE_API_KEY"] || "YOUR_API_KEY";
const substrate = new Substrate({ apiKey: apiKey });
```

In Python it will look like this:

```python
import os

from substrate import ComputeJSON, ComputeText, Substrate, sb


api_key = os.environ.get("SUBSTRATE_API_KEY") or "YOUR_API_KEY"
substrate = Substrate(api_key=api_key)
```

The first thing we'll need to do is setup our skeleton given a question. We're going to prompt an LLM
to generate this for us, then extract the outline from the generated text into a well-defined schema.

Here's what this could look like in TypeScript:

```typescript
const question = "What are some underrated olympic sports?";

const outlineText = new ComputeText({
prompt: sb.interpolate`
You’re an organizer responsible for only giving the outline (not the full content) for answering the question.
Provide the outline in a list of points (numbered 1., 2., 3., etc.) to answer the question.
Instead of writing a full sentence, each skeleton point should be very short with only 3∼5 words.

=== Question
${question}`,
});

const outlineList = new ComputeJSON({
prompt: sb.interpolate`Extract the numbered outline items from the following (do not keep the item number):\n ${outlineText.future.text}`,
json_schema: {
  type: "object",
  properties: {
    outline: {
      type: "array",
      minItems: 3,
      maxItems: 10,
      items: {
        type: "string",
      },
    },
  },
  required: ["outline"],
},
});

const outlineRes = await substrate.run(outlineList);
const outline = outlineRes.get(outlineList).json_object!.outline as string[];
```

In Python the code will look largely the same:

```python
question = "what are some underrated olympic sports?"

outline_text = ComputeText(
    prompt=f"""
You’re an organizer responsible for only giving the outline (not the full content) for answering the question.
Provide the outline in a list of points (numbered 1., 2., 3., etc.) to answer the question.
Instead of writing a full sentence, each skeleton point should be very short with only 3∼5 words.

=== Question
{question}`,
    """
)

outline_list = ComputeJSON(
    prompt =sb.format("""
Extract the numbered outline items from the following (do not keep the item number):

{text}""", text=outline_text.future.text),
    json_schema = {
      "type": "object",
      "properties": {
        "outline": {
          "type": "array",
          "minItems": 3,
          "maxItems": 10,
          "items": {
            "type": "string",
          },
        },
      },
      "required": ["outline"],
    },
)
res = substrate.run(outline_list)
outline = res.get(outline_list).json_object["outline"]
```

Once we have the skeleton generated, we can expand on each point with an LLM per item. These will be run
in paralell on Substrate. Then we can collect all the points and use another LLM to combine this content 
into a cohesive reply to the original question.

In TypeScript it will look like the following:

```typescript
const pointExpanders = outline.map((point) => {
return new ComputeText(
  {
    prompt: sb.interpolate`
You're responsible for continuing the writing of one and only one point in the overall answer to the following question.
Write it very shortly in 1∼2 sentence and do not continue with other points!

=== The question is
${question}

=== The outline of the answer is
${outline as any}

Continue and only continue the writing of point: ${point}.`,
  },
);
});

const combined = new ComputeText({
prompt: sb.interpolate`
  Rewrite the following into a fluid, cohesive answer to the question. 
  Make use of all the content already outlined.

  === Question
  ${question}

  === Outlined Content
  ${sb.concat(...pointExpanders.map((p) => sb.concat(p.future.text, "\n")))}`,
});

const res = await substrate.run(combined);
console.log(res.get(combined).text);
```

And in Python it will look similar:

```python
point_expanders = [
    ComputeText(
        prompt=f"""
You're responsible for continuing the writing of one and only one point in the overall answer to the following question.
Write it very shortly in 1∼2 sentence and do not continue with other points!

=== The question is
{question}

=== The outline of the answer is
{outline}

Continue and only continue the writing of point: {point}.`,
        outline"""
    )
    for point
    in outline
]

points = sb.concat(*[
    sb.concat(point.future.text, "\n")
    for point
    in point_expanders
])

combined = ComputeText(
    prompt = sb.format("""
Rewrite the following into a fluid, cohesive answer to the question. 
Make use of all the content already outlined.

=== Question
{question}

=== Outlined Content
{points}""", question=question, points=points)
)

res = substrate.run(combined)
print(res.get(combined).text)
```

We hope you find this technique useful and that Substrate helps you implement this with ease!
