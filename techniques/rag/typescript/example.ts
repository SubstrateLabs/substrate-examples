#!/usr/bin/env -S npx ts-node --transpileOnly
import {
  Substrate,
  FindOrCreateVectorStore,
  QueryVectorStore,
  sb,
  ComputeText,
  Box,
} from "substrate";

async function main() {
  const apiKey = process.env["SUBSTRATE_API_KEY"] || "YOUR_API_KEY";
  const substrate = new Substrate({ apiKey: apiKey });

  const getStore = new FindOrCreateVectorStore({
    collection_name: "almanac",
    model: "jina-v2",
  });

  const prompt = "Recipe for banana chiffon pie";

  const fetchSources = new QueryVectorStore({
    collection_name: getStore.future.collection_name,
    model: getStore.future.model,
    query_strings: [prompt],
    include_metadata: true,
  });

  const answerQuestion = new ComputeText({
    prompt: sb.interpolate`
      ${prompt}

      Use the reference materials from the farmers almanac provided below and cite page numbers.

      ${sb.jq(fetchSources.future.results, "[.[0][] | .metadata] | tostring")}
    `,
  });

  const start = logStart();
  const res = await substrate.run(answerQuestion);
  logEnd(start);

  console.log(`\x1b[94m${res.get(answerQuestion).text}\x1b[0m`);
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
