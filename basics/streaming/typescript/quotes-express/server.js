import express from "express";
import path from "node:path";
import { Readable } from "node:stream";
import { Substrate, ComputeText } from "substrate";

const app = express();
const PORT = 3000;
const SUBSTRATE_API_KEY = process.env["SUBSTRATE_API_KEY"];

app.use(express.static("static"));
app.set("views", "./static");

app.get("/", (req, res) => {
  res.render("index.html");
});

app.get("/quote", async (req, res) => {
  const substrate = new Substrate({ apiKey: SUBSTRATE_API_KEY });
  const node = new ComputeText({ prompt: "an inspirational programming quote" });
  const stream = await substrate.stream(node);
  res.writeHead(200, { "Content-Type": "text/event-stream" });
  Readable.from(stream.apiResponse.body).pipe(res);
});

app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
