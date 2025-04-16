from fastapi import APIRouter, HTTPException
from chatbot.chatbot import query_rag, query_status_progress

router = APIRouter()

@router.post("/query/")
async def ask_question(question: str):
    try:
        response = query_rag(question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/status/")
async def get_status(application_id: str):
    try:
        response = query_status_progress(application_id)
        return {"status": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))