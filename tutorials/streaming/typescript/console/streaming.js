import { Substrate, ComputeText } from "substrate";

const substrate = new Substrate({ apiKey: process.env["SUBSTRATE_API_KEY"] });

const node = new ComputeText({ prompt: "an inspirational programming quote" });

const stream = await substrate.stream(node);

for await (let message of stream) {
  if (message.node_id === node.id && message.object === "node.delta") {
    process.stdout.write(message.data.text);
  }
}
