# GenerateText in Typescript

To run this example,

```bash
# Set your API key as an environment variable.
# Get one here https://www.substrate.run/dashboard/keys if this is your first time.
export SUBSTRATE_API_KEY=<your Substrate API key>

# Navigate to the python example directory.
cd typescript
```

To run the example with tsx (default), run the following.

```bash
npx tsx ./example.ts
npx tsx ./example-multi.ts

# Or you can use the package.json scripts
npm run example
npm run example-multi
```

To run the example with Deno, uncomment the Deno sections in `example.ts` and
run the following.

```bash
deno run ./example.ts
deno run ./example-multi.ts
```
