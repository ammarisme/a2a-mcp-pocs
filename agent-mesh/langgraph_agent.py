import json
import requests
from fastapi import FastAPI, HTTPException
from python_a2a.discovery import DiscoveryClient
from shared_context import ContextModel
from simple_graph import run_graph

app = FastAPI()

disc = DiscoveryClient(agent_card=None)
disc.add_registry("http://localhost:8000")
_cached_agent_url: str | None = None

def get_agent_url() -> str:
    global _cached_agent_url
    if _cached_agent_url:
        return _cached_agent_url

    print("Agent discovery through registry")
    agents = disc.discover()
    for a in agents:
        if a.capabilities.get("google_a2a_compatible"):
            _cached_agent_url = a.url
            print("A2A compatible agent found.")
            return _cached_agent_url
    raise RuntimeError("No suitable A2A agent found")

@app.post("/orchestrate", response_model=ContextModel)
def orchestrate(ctx: ContextModel):
    try:
        print("Executing langgraph")
        # run the local node
        ctx = run_graph(ctx)

        # call the A2A agent
        agent_url = get_agent_url().rstrip("/") + "/a2a"
        payload = {
            "content": {"type": "text", "text": json.dumps(ctx.model_dump())},
            "role": "user",
            "conversation_id": ctx.userId
        }
        resp = requests.post(agent_url, json=payload, timeout=5)
        resp.raise_for_status()

        # extract the JSON from parts[]
        body = resp.json()
        parts = body.get("parts", [])
        if not parts:
            raise ValueError("No response parts received")
        text_part = next((p for p in parts if p.get("type") == "text"), parts[0])
        updated = json.loads(text_part["text"])

        # return a full ContextModel
        return ContextModel(**updated)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("langgraph_agent:app", host="0.0.0.0", port=9000)
