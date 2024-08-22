# Chat with an LLM

<details>
<summary>How to run this example</summary>
<br/>

```bash
# Set your API key as an environment variable.
export SUBSTRATE_API_KEY=ENTER_YOUR_KEY

# Run the TypeScript example

cd typescript                    # Navigate to the typescript example
npm install                      # Install dependencies
npm start                        # Run the example

# Run the Python example

# Using poetry

cd python                        # Navigate to the python example
poetry install                   # Install dependencies and build the example
poetry run main                  # Run the example
```

</details>

![hero](hero.png)

In this short tutorial we're going to look at how to setup a simple console app to chat with an LLM. 

At a high level, what we're doing is creating a loop where we:
1. Accept user input
2. Generate the LLM response (that includes the chat history in the context)
3. Update the chat history

Using Substrate we can interact with an LLM using the `ComputeText` node and when we construct the prompt
we will be including the chat history that includes both the user input and LLM responses.

In NodeJS we can use the following program:

```js
import readline from "node:readline";

import { Substrate, ComputeText } from "substrate";

const substrate = new Substrate({ apiKey: process.env["SUBSTRATE_API_KEY"] });

const message = (role, content) => ({ role, content });

const blue = (text) => `\x1b[34m${text}\x1b[0m`;

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const prompt = (log) => `
You are a friendly assistant. Have fun engaging in the conversation.

=== Rules
* Reply with just text
* No special formatting for your role in the text
* Ask engaging follow up questions when appropriate

=== Chat Log
${log.map((m) => `[${m.role}]: ${m.content}`).join("\n\n")}`;

const continueThread = (log) => {
  rl.question(`> `, async (userPrompt) => {
    log.push(message("user", userPrompt));

    const llm = new ComputeText({ prompt: prompt(log) });
    const stream = await substrate.stream(llm);

    process.stdout.write("\n");
    for await (let event of stream) {
      if (event.object === "node.delta") {
        process.stdout.write(blue(event.data.text));
      }
      if (event.object === "node.result") {
        process.stdout.write("\n\n");
        log.push(message("assistant", event.data.text));
      }
    }
    continueThread(log);
  });
};
console.log("=== Welcome to the chat! (use ^C to quit)");
continueThread([]);
```

Most of the program above is handling user inputs, writing outputs, and running our chat loop with a log of what's been said so far.

There's only a little bit of Substrate code required here to prompt an LLM and stream the response back.

In Python we can create a similar example that works the same way.

```python
import os
from dataclasses import dataclass

from substrate import ComputeText, Substrate

substrate = Substrate(api_key=os.environ.get("SUBSTRATE_API_KEY"))


@dataclass
class Message:
    role: str
    content: str


def blue(text):
    return f"\x1b[34m{text}\x1b[0m"


prompt = """
You are a friendly assistant. Have fun engaging in the conversation.

=== Rules
* Reply with just text
* No special formatting for your role in the text
* Ask engaging follow up questions when appropriate

=== Chat Log
{chat_log}"""


def continue_thread(log):
    user_prompt = input("> ")
    log.append(Message(role="user", content=user_prompt))

    chat_log = "\n".join([f"{m.role}: {m.content}" for m in log])

    llm = ComputeText(prompt=prompt.format(chat_log=chat_log))
    stream = substrate.stream(llm)

    print()
    for event in stream.iter():
        if event.data["object"] == "node.delta":
            print(blue(event.data["data"]["text"]), end="", flush=True)

        if event.data["object"] == "node.result":
            log.append(Message(role="assistant", content=event.data["data"]["text"]))

    print("\n")
    continue_thread(log)


def main():
    print("=== Welcome to the chat! (use ^C to quit)")
    continue_thread([])


if __name__ == "__main__":
    main()
```

We could extend these simple examples in many different ways to suit a new specific need. For example,
updating the prompts to guide the LLM responses toward a particular tone or personality. If there is 
data we'd like the LLM to reference we could incorportate some context from a relevant data source. Enjoy
exploring what's possible with Substrate.

