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
