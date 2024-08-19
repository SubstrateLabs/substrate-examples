"use server";

import { Substrate, ComputeText } from "substrate";

const SUBSTRATE_API_KEY = process.env["SUBSTRATE_API_KEY"];

const substrate = new Substrate({ apiKey: SUBSTRATE_API_KEY });

export async function POST() {
  const node = new ComputeText({ prompt: "an inspirational programming quote" });
  const stream = await substrate.stream(node);
  return new Response(stream.apiResponse.body, {
    headers: { "Content-Type": "text/event-stream" },
  });
}
