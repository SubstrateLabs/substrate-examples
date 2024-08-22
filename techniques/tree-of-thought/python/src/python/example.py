import os
import time
from substrate import Substrate, MultiComputeText, sb, ComputeJSON


def main():
    api_key = os.environ.get("SUBSTRATE_API_KEY") or "YOUR_API_KEY"
    substrate = Substrate(api_key=api_key)

    current_reasoning = MultiComputeText(
        prompt="""You are an expert at deduction and logical reasoning. You are trying to determine where someone is hiding in a game of hide-and-seek.
        They know the person started in the kitchen.
        Here is the layout of the property:
        The kitchen has only one exit - to the garden.
        The garden has two possible exits - the kitchen, and the garage.
        The garage itself has an exit back to the garden or to a hidden alleyway with many obstacles and trash cans therein.
        The door to the alleyway is cracked open.
        The alleyway exits to the street and out to the rest of the neighborhood.
        The person is not in the kitchen or the garden.
        Based on your current understanding, explain where you think the person is and why.""",
        num_choices=3,
    )

    text = sb.jq(current_reasoning.future.choices, 'map(.text) | join("\n\n")')
    prompt = sb.concat(
        """Three experts are discussing the reasoning behind where the target in a game of hide and seek is hiding.
        Based on the circumstances, they all must agree on the correct reasoning and location of that person.""",
        "\n\n",
        text,
    )
    best_choice = ComputeJSON(
        prompt=prompt,
        json_schema={
            "properties": {
                "state": {
                    "type": "string",
                    "description": "The currently agreed-upon location of the person",
                },
                "explanation": {
                    "type": "string",
                    "description": "The reasoning behind why that person is most likely in that location",
                },
                "rules": {
                    "type": "string",
                    "description": "The current rules and assumptions of the game being played",
                },
            },
        },
    )

    for _ in range(3):
        current_reasoning = MultiComputeText(
            prompt=sb.concat(
                "Using the following reasoning, update your understanding as well as possible:",
                "STATE:",
                best_choice.future.json_object.state,
                "_____________",
                "EXPLANATION:",
                best_choice.future.json_object.explanation,
                "_____________",
                "RULES:",
                best_choice.future.json_object.rules,
            ),
            num_choices=5,
        )

        text = sb.jq(current_reasoning.future.choices, 'map(.text) | join("\n\n")')
        prompt = sb.concat(
            """Three experts are discussing the reasoning behind why they believe someone is somewhere.
            Based on the circumstances, they all must agree on the correct reasoning and location of that person.""",
            "\n\n",
            text,
        )
        best_choice = ComputeJSON(
            prompt=prompt,
            json_schema={
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "The currently agreed-upon location of the person",
                    },
                    "explanation": {
                        "type": "string",
                        "description": "The reasoning behind why that person is most likely in that location",
                    },
                    "rules": {
                        "type": "string",
                        "description": "The current rules and assumptions of the game being played",
                    },
                },
                "required": ["state", "explanation"],
            },
        )
    start = log_start()
    res = substrate.run(best_choice)
    log_end(start)

    print(res.get(best_choice))


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
