# Sentiment Analysis

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

Sentiment analysis is used to extract and quantify feelings from text. It's used in many contexts such
as customer support, customer reviews, recommendations, and more.

In this example, we'll use LLMs via Substrate to build a simple sentiment analysis pipeline that will
output scores for how positive, negative, or neutral some given text is and use this to determine an
overall classification.

The first thing we're going to do is to is use an LLM to analyze some content and generate a report by
asking the LLM to write out it's interpretation of the text and score the text. This can be done with
the `ComputeText` node and some prompt engineering.

In TypeScript this could look like this:

```typescript
const message = "what a great product, NOT!";

const assess = new ComputeText({
  prompt: `
  Your job is to assess a piece of CONTENT on the underlying emotional sentiment it communicates.
  Please follow the RULES of the assignment and be mindful of the TIPS.

  === RULES
  Analyze the content and report on POSITIVE sentiment if there is any, NEUTRAL sentiment if there is any, and NEGATIVE sentiment if there is any.
  Record your rationale for your conclusions.

  Once you have done so, please assign a score for each:
  POSITIVE (0-100): ___
  NEUTRAL  (0-100): ___
  NEGATIVE (0-100): ___

  === TIPS
  * Sometimes content may seem positive when it is negative, for example when using sarcasm or negation
  * When the sentiment is mixed, do your best to represent that across the scores

  === CONTENT
  ${message}
  `,
  temperature: 0.2,
})
```

And similarly in Python it could look like this:

```python
message = "what a great product, NOT!"

assess = ComputeText(
    prompt=f"""
    Your job is to assess a piece of CONTENT on the underlying emotional sentiment it communicates.
    Please follow the RULES of the assignment and be mindful of the TIPS.

    === RULES
    Analyze the content and report on POSITIVE sentiment if there is any, NEUTRAL sentiment if there is any, and NEGATIVE sentiment if there is any.
    Record your rationale for your conclusions.

    Once you have done so, please assign a score for each:
    POSITIVE (0-100): ___
    NEUTRAL  (0-100): ___
    NEGATIVE (0-100): ___

    === TIPS
    * Sometimes content may seem positive when it is negative, for example when using sarcasm or negation
    * When the sentiment is mixed, do your best to represent that across the scores

    === CONTENT
    ${message}""",
    temperature=0.2,
)
```

The output of this node will be a `string` of the report, but next we can use a `ComputeJSON` node to extract
structured data from this report to be used in a real system.

In TypeScript the next step could look like this:

```typescript
const extract = new ComputeJSON({
  prompt: sb.interpolate`
  Your job is to extract the relevant details of the sentiment analysis REPORT.
  Please do so as accurately as possible and include a short summary of the rationale.

  === REPORT
  ${assess.future.text}
  `,
  json_schema: {
    type: "object",
    properties: {
      positive_score: { type: "integer", minimum: 0, maximum: 100 },
      neutral_score: { type: "integer", minimum: 0, maximum: 100 },
      negative_score: { type: "integer", minimum: 0, maximum: 100 },
      sentiment: { type: "string", enum: ["positive", "neutral", "negative"] },
      summary: { type: "string" },
    }
  }
})
```

Or in Python, like this:

```python
extract = ComputeJSON(
    prompt=sb.format(
        """
    Your job is to extract the relevant details of the sentiment analysis REPORT.
    Please do so as accurately as possible and include a short summary of the rationale.

    === REPORT
    ${report}
    """,
        report=assess.future.text,
    ),
    json_schema={
        "type": "object",
        "properties": {
            "positive_score": {"type": "integer", "minimum": 0, "maximum": 100},
            "neutral_score": {"type": "integer", "minimum": 0, "maximum": 100},
            "negative_score": {"type": "integer", "minimum": 0, "maximum": 100},
            "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
            "summary": {"type": "string"},
        },
    },
)
```

We're using a JSON Schema here to structure the outputs exactly how we want them and can ensure the fields
are constrained as we like. Note here that we're passing in the output of the previous node using the _future_
provided by the `assess` node we created. This way we can run the entire workflow with a single API request.

Finally we can run this graph like so in TypeScript:

```typescript
const res = await substrate.run(extract);
console.log(res.get(extract).json_object);
```

Or in Python:

```python
res = substrate.run(extract)
print(res.get(extract).json_object)
```

The final result will look like the following:

```json
{
  "positive_score": 0,
  "neutral_score": 0,
  "negative_score": 100,
  "sentiment": "negative",
  "summary": "The sentiment is primarily negative due to the use of sarcasm and negation in the phrase 'NOT!' at the end of the sentence."
}
```

You can build on this example further if you like. For example, perhaps there are other dimensions you would like to assess for or
perhaps there are more details you would like the LLM to pay closer attention too. You could even run the same pipeline multiple
times on the same data to collect some aggregated assessment of several passes.

We hope this example is helpful for you and that you enjoy working with Substrate as much as we do!
