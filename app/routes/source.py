from fastapi import APIRouter, Depends, Body, HTTPException
from bson import ObjectId
from typing import Any, List
from app.services.scrape import scrape_talents
from app.services.source_with_jd import scrape_talents_with_jd

router = APIRouter()

@router.post("/source")
async def source(
      job_role: str | None = Body(default=None),
      company: str | None = Body(default=None),
      education: str | None = Body(default=None),
      years_of_experience: str | None = Body(default=None),
      location: str | None = Body(default=None),
      additional_prompt: str | None = Body(default=None),
      num_results: int = Body(default=10)):

      print(job_role, company, education, years_of_experience, location, additional_prompt, num_results)

      if job_role is not None and job_role.strip() == "":
            job_role = None
      if company is not None and company.strip() == "":
            company = None
      if education is not None and education.strip() == "":
            education = None
      if years_of_experience is not None and years_of_experience.strip() == "":
            years_of_experience = None
      if location is not None and location.strip() == "":
            location = None
      if additional_prompt is not None and additional_prompt.strip() == "":
            additional_prompt = None

      if num_results>100:
            num_results=100

      results = scrape_talents(job_role, company, education, years_of_experience, location, additional_prompt, num_results)
      return results

@router.post("/sourceWithJD")
async def source_with_jd(
    job_description: str | None = Body(default=None),
    location: str | None = Body(default=None),
    num_results: int = Body(default=20)
):
    try:
        # Limit max results to 100
        if num_results > 100:
            num_results = 100

        # Normalize empty location to None
        if location is not None and location.strip() == "":
            location = None

        # Call the scraping function
        results = scrape_talents_with_jd(job_description, location, num_results)
        
        return results

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
