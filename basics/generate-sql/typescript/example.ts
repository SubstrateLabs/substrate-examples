import { GenerateCode, Substrate } from "substrate";
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
            onResolve(res.map((row) => {
              row.user_id = Number(row.user_id);
              return row;
            }));
          }
        });
      },
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
            onResolve(res.map((row) => {
              row.user_id = Number(row.user_id);
              row.tid = Number(row.tid);
              return row;
            }));
          }
        });
      },
    );
  });
}

function verbalize_table(name: string, table: object[]): string {
  return `
The table '${name}' has ${Object.keys(table[0]).length} columns. They are ${Object.keys(table[0]).join(", ")
    }.
Below is a sample of the data contained in this table.

${table.slice(0, 5).map((row) => JSON.stringify(row)).join("\n")}
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

  const apiKey = process.env["SUBSTRATE_API_KEY"] || "YOUR_API_KEY";
  const substrate = new Substrate({ apiKey: apiKey });

  const node = new GenerateCode({ prompt: prompt, language: "sql" });

  const start = logStart();
  const res = await substrate.run(node);
  logEnd(start);

  const code = res.get(node).code;
  console.log(`Prompt:\n${node.args.prompt}\n`);
  console.log(`Generated SQL code:\n${code}\n`);
  db.all(code, (err, res) => {
    if (err) console.error(err);
    else console.log(`SQL query result:\n${res.map(row => JSON.stringify(row)).join("\n")}\n`);
  });
}

main();

function logStart(): number {
  const start = Date.now();
  console.log("\x1b[94m֍ \x1b[34m Running... \x1b[0m");
  return start;
}

function logEnd(start: number) {
  const end = Date.now();
  const duration = end - start;
  const seconds = (duration / 1000).toFixed(2);
  console.log(`\x1b[92m֍ \x1b[32m Completed in ${seconds}s\x1b[0m`);
}
