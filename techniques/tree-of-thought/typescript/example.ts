import {
  ComputeText,
  MultiComputeText,
  Substrate,
  sb,
  Box,
  ComputeJSON,
} from "substrate";

// Uncomment the following line if using Deno
// import process from "node:process";

async function main() {
  const apiKey = process.env["SUBSTRATE_API_KEY"] || "YOUR_API_KEY";
  const substrate = new Substrate({
    apiKey: apiKey,
  });

  let currentReasoning = new MultiComputeText({
    prompt: `You are an expert at deduction and logical reasoning. You are trying to determine where someone is hiding in a game of hide-and-seek.
      They know the person started in the kitchen.
      Here is the layout of the property:
      The kitchen has only one exit - to the garden.
      The garden has two possible exits - the kitchen, and the garage.
      The garage itself has an exit back to the garden or to a hidden alleyway with many obstacles and trash cans therein.
      The door to the alleyway is cracked open.
      The alleyway exits to the street and out to the rest of the neighborhood.
      The person is not in the kitchen or the garden.
      Based on your current understanding, explain where you think the person is and why.`,
    num_choices: 3,
  });

  // @ts-ignore
  let text = sb.jq(
    currentReasoning.future.choices,
    'map(.text) | join("\n\n")'
  );
  let prompt = sb.interpolate`Three experts are discussing the reasoning behind where the target in a game of hide and seek is hiding. Based on the circumstances, they all must agree on the correct reasoning and location of that person.\n\n${text}`;
  let bestChoice = new ComputeJSON({
    prompt,
    json_schema: {
      properties: {
        state: {
          type: "string",
          description: "the currently agreed-upon location of the person",
        },
        explanation: {
          type: "string",
          description:
            "the reasoning behind why that person is most likely in that location",
        },
        rules: {
          type: "string",
          description:
            "the current rules and assumptions of the game being played",
        },
      },
    },
  });

  for (let i = 0; i < 3; i++) {
    currentReasoning = new MultiComputeText({
      prompt: sb.concat(
        "Using the following reasoning, update your understanding as well as possible:",
        "STATE:",
        // @ts-ignore
        bestChoice.future.json_object.get("state"),
        "_____________",
        "EXPLANATION:",
        bestChoice.future.json_object.get("explanation"),
        "_____________",
        "RULES:",
        bestChoice.future.json_object.get("rules")
      ),
      num_choices: 3,
    });

    text = sb.jq(currentReasoning.future.choices, 'map(.text) | join("\n\n")');
    prompt = sb.interpolate`Three experts are discussing the reasoning behind why they believe someone is somewhere. Based on the circumstances, they all must agree on the correct reasoning and location of that person.\n\n${text}`;
    bestChoice = new ComputeJSON({
      prompt,
      json_schema: {
        properties: {
          state: {
            type: "string",
            description: "the currently agreed-upon location of the person",
          },
          explanation: {
            type: "string",
            description:
              "the reasoning behind why that person is most likely in that location",
          },
          rules: {
            type: "string",
            description:
              "the current rules and assumptions of the game being played",
          },
        },
        required: ["state", "explanation"],
      },
    });
  }
  const start = logStart();
  const res = await substrate.run(bestChoice);
  logEnd(start);
  console.log(res.get(bestChoice));
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
