"""Example FastAPI server exposing the ReasoningLoop."""

from __future__ import annotations

from fastapi import FastAPI, Request

from aethermind.brain import Brain
from aethermind.goals import GoalManager
from aethermind.reasoning import ReasoningLoop
from aethermind.identity import Identity
from aethermind.llm import chat

app = FastAPI(title="AetherMind API")

identity = Identity.load("identity.yaml")
brain = Brain()
goals = GoalManager()
loop = ReasoningLoop(brain, goals)


@app.post("/reason/")
async def reason(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    # optionally use the LM Studio server to parse or expand the input
    llm_response = chat(
        [
            {"role": "system", "content": identity.purpose},
            {"role": "user", "content": user_input},
        ]
    )
    output = loop.cycle(llm_response)
    return {"output": output, "llm": llm_response}
