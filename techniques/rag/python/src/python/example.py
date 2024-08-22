import os
import time
from substrate import Substrate, ComputeText, FindOrCreateVectorStore, QueryVectorStore, sb


# This example demonstrates how to use the QueryVectorStore and ComputeText nodes to do Retrieval Augmented Generation (RAG)
# In this example we assume you have embedded The Old Farmer's almanac from the `embed-documents` example.
def main():
    api_key = os.environ.get("SUBSTRATE_API_KEY") or "YOUR_API_KEY"
    substrate = Substrate(api_key=api_key)

    prompt = "Recipe for banana chiffon pie"

    get_store = FindOrCreateVectorStore(collection_name="almanac", model="jina-v2")

    fetch_sources = QueryVectorStore(
        collection_name=get_store.future.collection_name,
        model=get_store.future.model,
        query_strings=[prompt],
        include_metadata=True,
    )

    template = """
        {{ prompt }}

        Use the reference materials from the farmers almanac provided below and cite page numbers.
        {% for item in results %}
            {{ item.metadata }}
        {% endfor %}
    """
    answer_question = ComputeText(prompt=sb.jinja(template, prompt=prompt, results=fetch_sources.future.results[0]))

    start = log_start()
    res = substrate.run(answer_question)
    log_end(start)

    print(f"""\033[94m{res.get(answer_question).text}\033[0m""")


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
