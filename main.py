from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel
from connectors.db import GraphDBBackend
from connectors.llm import LlmEngine

state = {}

class RequestBody(BaseModel):
    question: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Set up the local LLM And graph database
    state["db"] = GraphDBBackend("./location_data")
    state["llm"] = LlmEngine("./models/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf")
    yield
    
app = FastAPI(lifespan=lifespan)

@app.post("/")
async def query_llm(body: RequestBody):

    if body.question == "":
        return { "error": "Please specify a question" }

    query = state["llm"].generate_cypher_statement(state["db"].schema, body.question)
    results = state["db"].execute_query(query)

    return results
