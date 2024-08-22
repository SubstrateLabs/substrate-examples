import { ComputeText, ComputeJSON, Substrate, sb } from "substrate";

// Uncomment the following line if using Deno
// import process from "node:process";

async function main() {
  const apiKey = process.env["SUBSTRATE_API_KEY"] || "YOUR_API_KEY";
  const substrate = new Substrate({ apiKey: apiKey });

  const question = "What are some underrated olympic sports?";

  const outlineText = new ComputeText({
    prompt: sb.interpolate`
You’re an organizer responsible for only giving the outline (not the full content) for answering the question.
Provide the outline in a list of points (numbered 1., 2., 3., etc.) to answer the question.
Instead of writing a full sentence, each skeleton point should be very short with only 3∼5 words.

=== Question
${question}`,
  });

  const outlineList = new ComputeJSON({
    prompt: sb.interpolate`Extract the numbered outline items from the following (do not keep the item number):\n ${outlineText.future.text}`,
    json_schema: {
      type: "object",
      properties: {
        outline: {
          type: "array",
          minItems: 3,
          maxItems: 10,
          items: {
            type: "string",
          },
        },
      },
      required: ["outline"],
    },
  });

  const outlineRes = await substrate.run(outlineList);
  const outline = outlineRes.get(outlineList).json_object!.outline as string[];

  const pointExpanders = outline.map((point) => {
    return new ComputeText(
      {
        prompt: sb.interpolate`
You're responsible for continuing the writing of one and only one point in the overall answer to the following question.
Write it very shortly in 1∼2 sentence and do not continue with other points!

=== The question is
${question}

=== The outline of the answer is
${outline as any}

Continue and only continue the writing of point: ${point}.`,
      },
    );
  });

  const combined = new ComputeText({
    prompt: sb.interpolate`
      Rewrite the following into a fluid, cohesive answer to the question. 
      Make use of all the content already outlined.

      === Question
      ${question}

      === Outlined Content
      ${sb.concat(...pointExpanders.map((p) => sb.concat(p.future.text, "\n")))}`,
  });

  const start = logStart();
  console.log("Question:", question, "\n");
  const res = await substrate.run(combined);
  logEnd(start);
  console.log(res.get(combined).text);
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
