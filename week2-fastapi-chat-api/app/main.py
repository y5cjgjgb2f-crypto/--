from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel, Field


app = FastAPI(
    title="Week 2 FastAPI Chat API",
    description="A small API for learning HTTP, JSON, request bodies, and Swagger.",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, examples=["What is FastAPI?"])


class ChatResponse(BaseModel):
    answer: str
    question: str
    source: str



@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

'''依赖注入'''
async def common_parameters(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=60),
):
    return { "skip": skip, "limit": limit }

@app.get("/news/news_list")
def get_news_list(
    commons= Depends(common_parameters)
):
    # Placeholder implementation - replace with actual news fetching logic
    return commons

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    answer = f"You asked: {request.question}"
    return ChatResponse(
        answer=answer,
        question=request.question,
        source="fixed-response",
    )
