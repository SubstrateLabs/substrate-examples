import os
import time
from substrate import Substrate, MultiComputeText


def main():
    api_key = os.environ.get("SUBSTRATE_API_KEY") or "YOUR_API_KEY"
    substrate = Substrate(api_key=api_key)

    story = MultiComputeText(
        prompt="tell me a short 2-sentence story",
        num_choices=2,
    )

    start = log_start()
    res = substrate.run(story)
    log_end(start)

    print("1:", res.get(story).choices[0].text)
    print("2:", res.get(story).choices[1].text)


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
