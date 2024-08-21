# Generating SQL using Substrate

<details>
<summary>Expand details to see how to run this example.</summary><br/>

> [!NOTE]
> As of writting (Aug 2024), the `GenerateCode` node is supported but not yet documented since we just rolled it out. The SDK will be officially published soon. In the meantime, you can build the NPM package from Github, which we illustrated below.

```bash
# Set your API key as an environment variable.
# Get one here https://www.substrate.run/dashboard/keys if this is your first time.
export SUBSTRATE_API_KEY=<your Substrate API key>

# Navigate to the typescript example directory.
cd typescript
```

To run the example with tsx, run the following.

```bash
# Install Substrate from Github HEAD into /tmp/substrate
# You will not need to do this after we officially release GenerateCode.
npm run install-substrate
```

```bash
npm install
npx tsx ./example.ts

# Or you can use the package.json scripts
npm run start
```

This example does not work with Deno because DuckDB is not yet compatible as of writing.

</details><br/>

In this example, we demonstrate the ability to generate SQL using [Substrate](https://substrate.run)'s `GenerateCode` node.

We have two tables, a "Users" table and a "Transactions" table, recording the user information as well as their transactions. We generated some random data (by asking our LLMs :) and put them in the JSON files. Note that the JSON path is relative to where you invoke the Typescript script. Please adjust accordingly if you are not running from the same directory as this README.md file.

Here we use DuckDB to load the JSON files into in-memory tables.

```typescript
import duckdb from "duckdb";

async function load_users(db: duckdb.Database): Promise<any[]> {
  return new Promise((onResolve, onErr) => {
    db.run(
      "create table users as select * from read_json('./users.json');",
      (err) => {
        if (err) onErr(err);
        db.all("select * from users", (err, res) => {
          if (err) onErr(err);
          else {
            onResolve(
              res.map((row) => {
                row.user_id = Number(row.user_id);
                return row;
              })
            );
          }
        });
      }
    );
  });
}

async function load_transactions(db: duckdb.Database): Promise<any[]> {
  return new Promise((onResolve, onErr) => {
    db.run(
      "create table transactions as select * from read_json('./transactions.json');",
      (err) => {
        if (err) onErr(err);
        db.all("select * from transactions", (err, res) => {
          if (err) onErr(err);
          else {
            onResolve(
              res.map((row) => {
                row.user_id = Number(row.user_id);
                row.tid = Number(row.tid);
                return row;
              })
            );
          }
        });
      }
    );
  });
}

async function main() {
  const db = new duckdb.Database(":memory:");
  const users = await load_users(db);
  const transactions = await load_transactions(db);
}
```

Next we construct the prompt used for generating the code. In this simple example, we do the following prompting:

1. Describe how many tables we have and what their names are. This is to guide the LLMs to generate the correct table name.
2. We describe each table by showing the column names and some sample data.
3. Finally we add our intentions to the end.

```typescript
function verbalize_table(name: string, table: object[]): string {
  return `
The table '${name}' has ${Object.keys(table[0]).length} columns. They are ${Object.keys(
    table[0]
  ).join(", ")}.
Below is a sample of the data contained in this table.

${table
  .slice(0, 5)
  .map((row) => JSON.stringify(row))
  .join("\n")}
`;
}

async function main() {
  const db = new duckdb.Database(":memory:");
  const users = await load_users(db);
  const transactions = await load_transactions(db);

  const prompt = [
    "We have two tables, 'users' and 'transactions'",
    verbalize_table("users", users),
    verbalize_table("transactions", transactions),
    "Now I'd like to generate a SQL query to see the total amounts broken down by countries and sorted from the most amount to the least amount.",
  ].join("\n");
}
```

With the prompt, we're ready to call `GenerateCode`.

```typescript
const apiKey = process.env["SUBSTRATE_API_KEY"] || "YOUR_API_KEY";
const substrate = new Substrate({ apiKey: apiKey });
const node = new GenerateCode({ prompt: prompt, language: "sql" });
const res = await substrate.run(node);
const code = res.get(node).code;
```

The code can be verified with DuckDB.

```typescript
db.all(code, (err, res) => {
  if (err) console.error(err);
  else
    console.log(
      `SQL query result:\n${res.map((row) => JSON.stringify(row)).join("\n")}\n`
    );
});
```

If you run the example successfully, you may see outputs like this.

```
֍  Running...
֍  Completed in 1.17s
```

```
Prompt:
We have two tables, 'users' and 'transactions'

The table 'users' has 3 columns. They are user_id, name, country_code.
Below is a sample of the data contained in this table.

{"user_id":1,"name":"Alice","country_code":"US"}
{"user_id":2,"name":"Bob","country_code":"CA"}
{"user_id":3,"name":"Charlie","country_code":"UK"}
{"user_id":4,"name":"David","country_code":"AU"}
{"user_id":5,"name":"Eva","country_code":"DE"}


The table 'transactions' has 4 columns. They are tid, user_id, amount, timestamp.
Below is a sample of the data contained in this table.

{"tid":101,"user_id":1,"amount":50,"timestamp":"2023-08-15T10:30:00.000Z"}
{"tid":102,"user_id":3,"amount":25.5,"timestamp":"2023-08-16T14:15:00.000Z"}
{"tid":103,"user_id":2,"amount":100,"timestamp":"2023-08-17T09:45:00.000Z"}
{"tid":104,"user_id":5,"amount":75.25,"timestamp":"2023-08-18T18:00:00.000Z"}
{"tid":105,"user_id":4,"amount":30,"timestamp":"2023-08-19T12:30:00.000Z"}

Now I'd like to generate a SQL query to see the total amounts broken down by countries and sorted from the most amount to the least amount.
```

```
Generated SQL code:
SELECT
    u.country_code,
    SUM(t.amount) AS total_amount
FROM
    users u
JOIN
    transactions t ON u.user_id = t.user_id
GROUP BY
    u.country_code
ORDER BY
    total_amount DESC;
```

```
SQL query result:
{"country_code":"BR","total_amount":120}
{"country_code":"US","total_amount":110.75}
{"country_code":"UK","total_amount":105.7}
{"country_code":"CA","total_amount":100}
{"country_code":"JP","total_amount":90}
{"country_code":"DE","total_amount":75.25}
{"country_code":"FR","total_amount":45.5}
{"country_code":"AU","total_amount":30}
```
