import os
import sys
import time

import duckdb
import pandas as pd
from loguru import logger
from substrate import GenerateCode, Substrate


def load_users() -> pd.DataFrame:
    return duckdb.read_csv("./src/generatesql/users.csv").df()


def load_transactions() -> pd.DataFrame:
    return duckdb.read_csv("./src/generatesql/transactions.csv").df()


def verbalize_df(name: str, df: pd.DataFrame) -> str:
    return f"""
The table '{name}' has {len(df.columns)} columns. They are {list(df.columns)}.
Below is a sample of the data contained in this table.

{df.head()}
"""


def logging(msg: str):
    logger.opt(colors=True).info(msg)


def main():
    logger.remove()
    logger.add(
        sys.stdout, colorize=True, format="<green>֍ {time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{message}</level>"
    )

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

    api_key = os.environ.get("SUBSTRATE_API_KEY") or "YOUR_API_KEY"
    substrate = Substrate(api_key=api_key)

    node = GenerateCode(prompt=prompt, language="sql")

    start = log_start()
    res = substrate.run(node)
    log_end(start)

    code = res.get(node).code
    logging("<blue>Prompt</blue>\n" + node.args.get("prompt"))
    logging("<blue>Generated SQL code</blue>\n" + code)
    logging("<blue>SQL query result</blue>\n" + str(duckdb.sql(code).df()))


def log_start():
    start = time.time()
    logging("<blue>Running ...</blue>")
    return start


def log_end(start):
    end = time.time()
    duration = end - start
    seconds = f"{duration:.2f}"
    logging(f"<blue>Completed in {seconds}s</blue>")


if __name__ == "__main__":
    main()
