import { ComputeText, ComputeJSON, Substrate, sb } from "substrate";

// Uncomment the following line if using Deno
// import process from "node:process";

async function main() {
  const apiKey = process.env["SUBSTRATE_API_KEY"] || "YOUR_API_KEY";
  const substrate = new Substrate({ apiKey: apiKey });

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

  const start = logStart();
  const res = await substrate.run(extract);
  logEnd(start);

  console.log(res.get(extract).json_object);
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
