import { Substrate, ComputeText } from "substrate";

const substrate = new Substrate({ apiKey: process.env["SUBSTRATE_API_KEY"] });

const node = new ComputeText({ prompt: "an inspirational programming quote" });

const res = await substrate.run(node);
const text = res.get(node).text;

process.stdout.write(text);
