# Simple NextJS Example

This project is an example that creates a simple NextJS web app that demonstrates streaming an LLM response from a route handler to a client component.

```sh
# install the dependencies (substrate)
npm install

# set your Substrate API Key
export SUBSTRATE_API_KEY=<your-api-key>

# run the server
npm run dev

# view the page
open http://localhost:3000
```

## About the project

### `app/quote/route.ts`

This file contains the route handler used to fetch the LLM response from Substrate. We're using the route handler here so that we can produce an event-stream for our client code to consume.

### `app/Example.tsx`

This file contains our client component with a UI for fetching the stream from our route handler and rendering the stream chunks as they arrive.
