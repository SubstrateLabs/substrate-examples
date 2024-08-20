# Streaming to console example

This example demonstrates a simple Substrate request that generates text and writes it to the console.

In `non-streaming.js` you can see what this code looks like without streaming and compare to the streaming version in `streaming.js`.

To run these examples you might have a Substrate account and an API key to use. API keys are found in the [dashboard][(https://www.substrate.run/dashboard/keys).

```sh
# setup project
npm install

# set Substrate API in environment
export SUBSTRATE_API_KEY=<your-api-key>

# run non-streaming example (non-streaming.js)
npm run non-streaming

# run streaming example (streaming.js)
npm run streaming
```
