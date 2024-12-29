from fastapi import APIRouter, Depends, Body, HTTPException
from bson import ObjectId
from typing import Any, List

router = APIRouter()

@router.post("/source")
async def source(
    job_role: Any | None = Body(default=None),
    company: str | None = Body(default=None),
    education: str | None = Body(default=None),
    years_of_experience: str | None = Body(default=None),
    location: str | None = Body(default=None),
    additional_prompt: str | None = Body(default=None),
    num_results: int = Body(default=10)
    ):
    print(job_role, company, education, years_of_experience, 
          location, additional_prompt, num_results)
    return {
        "job_role": job_role,
        "company": company,
        "education": education,
        "years_of_experience": years_of_experience,
        "location": location,
        "additional_prompt": additional_prompt,
        "num_results": num_results
    }