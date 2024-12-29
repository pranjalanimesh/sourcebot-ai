from fastapi import APIRouter, Depends, Body, HTTPException
from bson import ObjectId
from typing import Any, List

router = APIRouter()

@router.get("/health")
async def health():
    return {"message": "Healthy!"}
