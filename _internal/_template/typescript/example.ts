#!/usr/bin/env -S npx ts-node --transpileOnly
import { Substrate, ComputeText, sb } from "substrate";

async function main() {
  const apiKey = process.env["SUBSTRATE_API_KEY"] || "YOUR_API_KEY";
  const substrate = new Substrate({ apiKey: apiKey });

  const story = new ComputeText({ prompt: "tell me a short 2-sentence story" });

  const start = logStart();
  const res = await substrate.run(story);
  logEnd(start);

  const summaryOut = res.get(story);
  console.log(summaryOut.text);
}

main();

function logStart(): number {
  const start = Date.now();
  console.log("\x1b[94m֍ \x1b[34m Running... \x1b[0m");
  return start;
}

function logEnd(start: number) {
  const end = Date.now();
  const duration = end - start;
  const seconds = (duration / 1000).toFixed(2);
  console.log(`\x1b[92m֍ \x1b[32m Completed in ${seconds}s\x1b[0m`);
}
