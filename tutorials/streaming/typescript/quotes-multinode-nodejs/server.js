import http from "node:http";
import fs from "node:fs";
import { Readable } from "node:stream";
import { Substrate, ComputeText, sb } from "substrate";

const SUBSTRATE_API_KEY = process.env["SUBSTRATE_API_KEY"];
const PORT = 3000;

// Create the server
const server = http.createServer(async (req, res) => {
  console.log(new Date(), "New request", req.url);
  // Serve the client side JS
  if (req.url.startsWith("/static/script.js")) {
    const script = fs.readFileSync("./static/script.js");
    res.writeHead(200, { "Content-Type": "application/javascript" });
    res.end(script);
    return;
  }

  // Serve the streaming Substrate content
  if (req.url.startsWith("/quote")) {
    try {
      const substrate = new Substrate({ apiKey: SUBSTRATE_API_KEY });
      const quote = new ComputeText({ prompt: "an inspirational programming quote" }, { id: "english", hide: true });
      const french = new ComputeText({ prompt: sb.concat("translate the following into french: ", quote.future.text) }, { id: "french" })
      const stream = await substrate.stream(french);
      res.writeHead(200, { "Content-Type": "text/event-stream" });
      Readable.from(stream.apiResponse.body).pipe(res);
      return;
    } catch(err) {
      console.error(err);
    }
  }

  // Serve the HTML page
  if (req.url.startsWith("/")) {
    const html = fs.readFileSync("./static/index.html");
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(html);
    return;
  }
});

// Start the server
server.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
