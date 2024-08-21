# Generating SQL using Substrate

<details>
<summary>Expand details to see how to run this example.</summary><br/>

```bash
# Set your API key as an environment variable.
# Get one here https://www.substrate.run/dashboard/keys if this is your first time.
export SUBSTRATE_API_KEY=<your Substrate API key>

# Navigate to the python example directory.
cd python
```

To run the example with Poetry (default), run the following.

```bash
poetry install
poetry run main
```

To run the example with Rye, comment out the Poetry sections and uncomment the Rye sections in `pyproject.toml` and run the following.

```bash
rye sync
rye run main
```

</details><br/>

In this example, we demonstrate the ability to generate SQL using [Substrate](https://substrate.run)'s `GenerateCode` node.

> [!NOTE]
> As of writting (Aug 2024), the `GenerateCode` node is supported but not yet documented since we just rolled it out. The SDK will be officially published soon.

We have two tables, a "Users" table and a "Transactions" table, recording the user information as well as their transactions. We generated some random data (by asking our LLMs :) and put them in the CSV files. Note that the CSV path is relative to where you invoke the Python script. Please adjust accordingly if you are not running from the same directory as this README.md file.

```python
import duckdb
import pandas as pd


def load_users() -> pd.DataFrame:
    return duckdb.read_csv("./src/generatesql/users.csv").df()


def load_transactions() -> pd.DataFrame:
    return duckdb.read_csv("./src/generatesql/transactions.csv").df()
```

Next we construct the prompt used for generating the code. In this simple example, we do the following prompting:

1. Describe how many tables we have and what their names are. This is to guide the LLMs to generate the correct table name.
2. We describe each table by showing the column names and some sample data.
3. Finally we add our intentions to the end.

```python
def verbalize_df(name: str, df: pd.DataFrame) -> str:
    return f"""
The table '{name}' has {len(df.columns)} columns. They are {list(df.columns)}.
Below is a sample of the data contained in this table.

{df.head()}
"""

def main():
    users = load_users()
    transactions = load_transactions()
    prompt = "\n".join(
        [
            "I have two tables, 'users' and 'transactions'.",
            verbalize_df("users", users),
            verbalize_df("transactions", transactions),
            "Now I'd like to generate a SQL query to see the total amounts broken down by countries and sorted from the most amount to the least amount.",
        ]
    )
```

With the prompt, we're ready to call `GenerateCode`.

```python
api_key = os.environ.get("SUBSTRATE_API_KEY")
substrate = Substrate(api_key=api_key)
node = GenerateCode(prompt=prompt, language="sql")
res = substrate.run(node)
code = res.get(node).code
```

The code can be verified with DuckDB.

```python
# Make sure these two variables are in the scope.
#
# users = load_users()
# transactions = load_transactions()

print(duckdb.sql(code).df())
```

If you run the example successfully, you may see outputs like this.

```txt
֍ 2024-08-19 16:07:45.556 Running ...
֍ 2024-08-19 16:07:46.585 Completed in 1.03s
```

```txt
֍ 2024-08-19 16:07:46.587 Prompt
I have two tables, 'users' and 'transactions'.

The table 'users' has 3 columns. They are ['user_id', 'user_name', 'country_code'].
Below is a sample of the data contained in this table.

   user_id user_name country_code
0        1     Alice           US
1        2       Bob           CA
2        3   Charlie           UK
3        4     David           AU
4        5       Eva           DE


The table 'transactions' has 4 columns. They are ['tid', 'user_id', 'timestamp', 'amount'].
Below is a sample of the data contained in this table.

   tid  user_id           timestamp  amount
0  101        1 2023-05-15 10:30:00   50.00
1  102        1 2023-06-20 14:15:00   75.50
2  103        2 2023-07-05 09:45:00   30.00
3  104        3 2023-08-10 18:00:00   60.25
4  105        1 2023-09-02 12:30:00  100.00

Now I'd like to generate a SQL query to see the total amounts broken down by countries and sorted from the most amount to the least amount.
```

```txt
֍ 2024-08-19 16:07:46.588 Generated SQL code
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

```txt
֍ 2024-08-19 16:07:46.611 SQL query result
  country_code  total_amount
0           US        225.50
1           AU        215.50
2           CA        141.00
3           UK         60.25
4           DE         40.80
```
