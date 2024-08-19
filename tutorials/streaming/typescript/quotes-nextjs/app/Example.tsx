"use client";
import { useState } from "react";
import { sb } from "substrate";

export function Example() {
  const [quote, setQuote] = useState<string>("");
  const getQuote = async (e: any) => {
    e.preventDefault();
    const response = await fetch("/quote", { method: "POST" });
    setQuote("");
    const stream = await sb.streaming.fromSSEResponse(response);

    for await (let message of stream) {
      if (message.object === "node.delta") {
        setQuote((state) => state + message.data.text);
      }
    }
  };

  return (
    <>
      <button onClick={getQuote}>Get a quote</button>
      <article>{quote}</article>
    </>
  );
}
