import os
from dataclasses import dataclass

from substrate import ComputeText, Substrate

substrate = Substrate(api_key=os.environ.get("SUBSTRATE_API_KEY"))


@dataclass
class Message:
    role: str
    content: str


def blue(text):
    return f"\x1b[34m{text}\x1b[0m"


prompt = """
You are a friendly assistant. Have fun engaging in the conversation.

=== Rules
* Reply with just text
* No special formatting for your role in the text
* Ask engaging follow up questions when appropriate

=== Chat Log
{chat_log}"""


def continue_thread(log):
    user_prompt = input("> ")
    log.append(Message(role="user", content=user_prompt))

    chat_log = "\n".join([f"{m.role}: {m.content}" for m in log])

    llm = ComputeText(prompt=prompt.format(chat_log=chat_log))
    stream = substrate.stream(llm)

    print()
    for event in stream.iter():
        if event.data["object"] == "node.delta":
            print(blue(event.data["data"]["text"]), end="", flush=True)

        if event.data["object"] == "node.result":
            log.append(Message(role="assistant", content=event.data["data"]["text"]))

    print("\n")
    continue_thread(log)


def main():
    print("=== Welcome to the chat! (use ^C to quit)")
    continue_thread([])


if __name__ == "__main__":
    main()
