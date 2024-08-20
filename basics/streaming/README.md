# Streaming

<details>
    <summary>How to run this example</summary>

```bash
# Set your API key as an environment variable.
export SUBSTRATE_API_KEY=ENTER_YOUR_KEY

# Run the TypeScript + NextJS example
cd typescript/quotes-nextjs     # Navigate to the typescript example
npm install                     # Install dependencies
npm run dev                     # Run the example
open http://127.0.0.1:3000      # View the web app

# Run the Python + FastAPI example
# Note: First install dependencies in the root examples directory.
cd python/quotes-fastapi        # Navigate to the python example
poetry install                  # Install dependencies
poetry run fastapi dev main.py  # Run the example
open http://127.0.0.1:8000      # View the web app
```

</details>

![hero](hero.png)

Substrate supports streaming responses in order to help improve the UX of your application by reducing the time it takes before a user sees a response.

The prevailing method of implementing streaming amongst inference providers is via Server-Sent Events and this is what we have chosen due to it's
widespread support and simple API.

We've designed our streaming API to work intuitively with the graph-oriented nature of the Substrate system. As a result we will stream back
messages for every node in the graph you run and messages relating to the graph as a whole. For many models we only support streaming back the final
result from a node, but for most LLM nodes we will also stream incremental chunks as the result is produced. We'll use the `ComputeText` node the the
examples here which emits these chunks within the delta message in the response stream.

In this article we're going to step through the process of making a streaming API request to Substrate and displaying streamed content to the user
in a web frontend. This example will focus on using NextJS and FastAPI, but there are other code samples included for some other popular alternatives.

First, let's take a look at making a streaming request with a single-node graph.

In TypeScript this looks like the following,

```typescript
import { Substrate, ComputeText } from "substrate";

const substrate = new Substrate({ apiKey: process.env["SUBSTRATE_API_KEY"] });

const node = new ComputeText({ prompt: "an inspirational programming quote" });

const stream = await substrate.stream(node);

for await (let message of stream) {
  if (message.node_id === node.id && message.object === "node.delta") {
    process.stdout.write(message.data.text);
  }
}
```

And when using Python it looks like this,

```python
import os

from substrate import ComputeText, Substrate

substrate = Substrate(api_key=os.environ.get("SUBSTRATE_API_KEY"))

node = ComputeText(prompt="an inspirational programming quote")

stream = substrate.stream(node)

for message in stream.iter():
    if message.data["object"] == "node.delta":
        print(message.data["data"]["text"], end="")
```

Because we're only using a single node, we know here that every `node.delta` message was produced by our single node. Every message also contains
the `node_id` - which we can use to identify messages from different nodes, but we're going to keep this example simple with one node.

When building an application that exposes the streaming result of a Substrate graph, what we will need to do is have our backend expose an endpoint
that reponds with a `text/event-stream`.

When using NextJS you will use a route handler to do so and it will look like this:

```typescript
"use server";

import { Substrate, ComputeText } from "substrate";

const SUBSTRATE_API_KEY = process.env["SUBSTRATE_API_KEY"];

const substrate = new Substrate({ apiKey: SUBSTRATE_API_KEY });

export async function POST() {
  const node = new ComputeText({
    prompt: "an inspirational programming quote",
  });
  const stream = await substrate.stream(node);
  return new Response(stream.apiResponse.body, {
    headers: { "Content-Type": "text/event-stream" },
  });
}
```

When using FastAPI it will look like this:

```python
import os

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from substrate import ComputeText, Substrate

app = FastAPI()

@app.get("/quote")
def quote():
    substrate = Substrate(api_key=os.environ.get("SUBSTRATE_API_KEY"))
    node = ComputeText(prompt="an inspirational programming quote")
    stream = substrate.stream(node)
    return StreamingResponse(stream.iter_events(), media_type="text/event-stream")
```

In the TypeScript example we're accessing the response body from the Substrate API and using this stream in the response directly, and in
the Python example we're exposing an iterator that produces formatted Server-Sent Event messages that can be used in the `StreamingResponse`.

Once these endpoints are setup we need to consume these streams on our web front end. In the following examples we've implemented a
simple UI to make the request and as the stream is recieved we upate the content the user is shown one chunk at a time.

In our NextJS example we're able to use the `substrate` TypeScript SDK, which exposes a helper method for parsing Server-Sent Event messages.
This makes it a little easier to deal with a streaming response in a similar we are on the server.

```tsx
"use client";
import { useState } from "react";
import { sb } from "substrate";

export function Example() {
  const [quote, setQuote] = useState<string>("");
  const getQuote = async (e: any) => {
    e.preventDefault();
    const response = await fetch("/quote", { method: "POST" });
    setQuote("");
    const stream = await sb.streaming.fromSSEResponse(response);

    for await (let message of stream) {
      if (message.object === "node.delta") {
        setQuote((state) => state + message.data.text);
      }
    }
  };

  return (
    <>
      <button onClick={getQuote}>Get a quote</button>
      <article>{quote}</article>
    </>
  );
}
```

In our FastAPI example we're not using a JS bundler, but instead are demonstrating how this might work when using Vanilla JS and some built-in web APIs
to accomplish the same task. We're using the `EventSource` object to handle the connection and event-stream parsing, but we'll also need to use `JSON.parse` on
the message data since we use a structured format for encoding the message contents there. Lastly, we make sure to `close()` the `EventSource`
once we receive the final message so that we do not make additional stream requests.

```javascript
document.addEventListener("DOMContentLoaded", () => {
  const output = document.getElementById("output");

  const button = document.getElementById("button");
  button.addEventListener("click", async (e) => {
    output.innerText = "";

    const sse = new EventSource("/quote");

    sse.addEventListener("message", (e) => {
      const message = JSON.parse(e.data);
      if (message.object === "node.delta") {
        // when we have a delta message, append the text data to our output element
        output.innerText += message.data.text;
      }
      if (message.object === "graph.result") {
        // last message is the graph result.
        sse.close();
      }
    });
  });
});
```
