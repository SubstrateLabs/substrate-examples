import os
import time
from substrate import FindOrCreateVectorStore, MultiEmbedText, SplitDocument, Substrate


# This example demonstrates how to
def main():
    api_key = os.environ.get("SUBSTRATE_API_KEY") or "YOUR_API_KEY"
    substrate = Substrate(api_key=api_key)

    create_store = FindOrCreateVectorStore(collection_name="almanac", model="jina-v2")

    split_doc = SplitDocument(
        uri="https://upload.wikimedia.org/wikipedia/commons/8/8a/The_Old_farmer%27s_almanac_%28IA_oldfarmersalmana1950unse%29.pdf",
    )

    embed_doc = MultiEmbedText(
        collection_name=create_store.future.collection_name,
        model=create_store.future.model,
        items=split_doc.future.items
    )

    start = log_start()
    res = substrate.run(embed_doc)
    log_end(start)

    create_store_result = res.get(create_store)
    embed_result = res.get(embed_doc)

    print(
f"""
\033[94m
Created {len(embed_result.embeddings)} embeddings
in collection {create_store_result.collection_name}
with model {create_store_result.model}
\033[0m
"""
    )


def log_start():
    start = time.time()
    print("\033[94m֍ \033[34mRunning...\033[0m")
    return start


def log_end(start):
    end = time.time()
    duration = end - start
    seconds = f"{duration:.2f}"
    print(f"\033[92m֍ \033[32mCompleted in {seconds}s\033[0m")


if __name__ == "__main__":
    main()
