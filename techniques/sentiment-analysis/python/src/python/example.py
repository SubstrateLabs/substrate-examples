import os
import time

from substrate import ComputeJSON, ComputeText, Substrate, sb


def main():
    api_key = os.environ.get("SUBSTRATE_API_KEY") or "YOUR_API_KEY"
    substrate = Substrate(api_key=api_key)

    message = "what a great product, NOT!"

    assess = ComputeText(
        prompt=f"""
        Your job is to assess a piece of CONTENT on the underlying emotional sentiment it communicates.
        Please follow the RULES of the assignment and be mindful of the TIPS.

        === RULES
        Analyze the content and report on POSITIVE sentiment if there is any, NEUTRAL sentiment if there is any, and NEGATIVE sentiment if there is any.
        Record your rationale for your conclusions.

        Once you have done so, please assign a score for each:
        POSITIVE (0-100): ___
        NEUTRAL  (0-100): ___
        NEGATIVE (0-100): ___

        === TIPS
        * Sometimes content may seem positive when it is negative, for example when using sarcasm or negation
        * When the sentiment is mixed, do your best to represent that across the scores

        === CONTENT
        ${message}""",
        temperature=0.2,
    )

    extract = ComputeJSON(
        prompt=sb.format(
            """
        Your job is to extract the relevant details of the sentiment analysis REPORT.
        Please do so as accurately as possible and include a short summary of the rationale.

        === REPORT
        ${report}
        """,
            report=assess.future.text,
        ),
        json_schema={
            "type": "object",
            "properties": {
                "positive_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "neutral_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "negative_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
                "summary": {"type": "string"},
            },
        },
    )

    start = log_start()
    res = substrate.run(extract)
    log_end(start)

    print(res.get(extract).json_object)


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
