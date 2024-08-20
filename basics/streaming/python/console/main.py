import os

from substrate import ComputeText, Substrate

substrate = Substrate(api_key=os.environ.get("SUBSTRATE_API_KEY"))

node = ComputeText(prompt="an inspirational programming quote")

stream = substrate.stream(node)

for message in stream.iter():
    if message.data["object"] == "node.delta":
        print(message.data["data"]["text"], end="")
