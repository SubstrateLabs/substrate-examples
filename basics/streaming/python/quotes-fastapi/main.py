import os

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from substrate import ComputeText, Substrate

app = FastAPI()

@app.get("/quote")
def quote():
    substrate = Substrate(api_key=os.environ.get("SUBSTRATE_API_KEY"))
    node = ComputeText(prompt="an inspirational programming quote")
    stream = substrate.stream(node)
    return StreamingResponse(stream.iter_events(), media_type="text/event-stream")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="static", html=True), name="index")
