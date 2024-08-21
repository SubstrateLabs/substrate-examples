document.addEventListener("DOMContentLoaded", () => {
  const output = document.getElementById("output");

  const button = document.getElementById("button");
  button.addEventListener("click", async (e) => {
    output.innerText = "";

    const sse = new EventSource("/quote");

    sse.addEventListener("message", (e) => {
      const message = JSON.parse(e.data);
      if (message.object === "node.delta") {
        // when we have a delta message, append the text data to our output element
        output.innerText += message.data.text;
      }
      if (message.object === "graph.result") {
        // last message is the graph result.
        sse.close();
      }
    });
  });
});
