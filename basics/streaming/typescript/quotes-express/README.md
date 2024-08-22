# Simple NodeJS streaming example using Express

This project is an example that creates a simple web app that streams an LLM response to a web app using NodeJS & Express.

This example demonstrates how you could integrate a streaming response from Substrate into a basic web server and use an `EventStream` from
a website.

```sh
# install the dependencies (substrate)
npm install

# set your Substrate API Key
export SUBSTRATE_API_KEY=<your-api-key>

# run the server
npm start

# view the page
open http://localhost:3000
```

## About the project

### `server.js`

This file contains a Express based server that serves an HTML page, a supporting JavaScript file, and an endpoint that streams back a Substrate response.

### `static/index.html`

This file is a simple HTMl document that sets up a couple of elements for the demo. A `<button>` for requesting a stream and an `<article>` that we'll put the stream chunks in as they arrive.

### `static/script.js`

This file handles the client side logic that requests the event stream from the server, and appends the message content to the page.
