#!/usr/bin/env -S npx ts-node --transpileOnly
import {
  Substrate,
  FindOrCreateVectorStore,
  SplitDocument,
  MultiEmbedText,
} from "substrate";

async function main() {
  const apiKey = process.env["SUBSTRATE_API_KEY"] || "YOUR_API_KEY";
  const substrate = new Substrate({ apiKey: apiKey });

  const createStore = new FindOrCreateVectorStore({
    collection_name: "almanac",
    model: "jina-v2",
  });

  const splitDoc = new SplitDocument({
    uri: "https://upload.wikimedia.org/wikipedia/commons/8/8a/The_Old_farmer%27s_almanac_%28IA_oldfarmersalmana1950unse%29.pdf",
  });

  const embedDoc = new MultiEmbedText({
    collection_name: createStore.future.collection_name,
    model: createStore.future.model,
    items: splitDoc.future.items,
  });

  const start = logStart();
  const res = await substrate.run(embedDoc);
  logEnd(start);

  const createStoreResult = res.get(createStore);
  const embedResult = res.get(embedDoc);
  console.log(
    `
\x1b[94m
Created ${embedResult.embeddings.length} embeddings
in collection ${createStoreResult.collection_name}
with model ${createStoreResult.model}
\x1b[0m
    `
  );
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
