import os
import time

from substrate import ComputeJSON, ComputeText, Substrate, sb


def main():
    api_key = os.environ.get("SUBSTRATE_API_KEY") or "YOUR_API_KEY"
    substrate = Substrate(api_key=api_key)

    question = "what are some underrated olympic sports?"

    outline_text = ComputeText(
        prompt=f"""
You’re an organizer responsible for only giving the outline (not the full content) for answering the question.
Provide the outline in a list of points (numbered 1., 2., 3., etc.) to answer the question.
Instead of writing a full sentence, each skeleton point should be very short with only 3∼5 words.

=== Question
{question}`,
        """
    )

    outline_list = ComputeJSON(
        prompt =sb.format("""
Extract the numbered outline items from the following (do not keep the item number):

{text}""", text=outline_text.future.text),
        json_schema = {
          "type": "object",
          "properties": {
            "outline": {
              "type": "array",
              "minItems": 3,
              "maxItems": 10,
              "items": {
                "type": "string",
              },
            },
          },
          "required": ["outline"],
        },
    )
    res = substrate.run(outline_list)
    outline = res.get(outline_list).json_object["outline"]

    point_expanders = [
        ComputeText(
            prompt=f"""
You're responsible for continuing the writing of one and only one point in the overall answer to the following question.
Write it very shortly in 1∼2 sentence and do not continue with other points!

=== The question is
{question}

=== The outline of the answer is
{outline}

Continue and only continue the writing of point: {point}.`,
            outline"""
        )
        for point
        in outline
    ]

    points = sb.concat(*[
        sb.concat(point.future.text, "\n")
        for point
        in point_expanders
    ])

    combined = ComputeText(
        prompt = sb.format("""
Rewrite the following into a fluid, cohesive answer to the question. 
Make use of all the content already outlined.

=== Question
{question}

=== Outlined Content
{points}""", question=question, points=points)
    )

    start = log_start()
    res = substrate.run(combined)
    log_end(start)

    print(res.get(combined).text)


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
