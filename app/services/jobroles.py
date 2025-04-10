from typing import List
from pydantic import BaseModel, Field
import ell
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class JobRolesModel(BaseModel):
    job_roles: List[str] = Field(..., title="List of Job Roles")

ell.init()

@ell.complex(model="gpt-4o", response_format=JobRolesModel, temperature=0.5, client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
def job_roles(user_query: str) -> JobRolesModel:
    """You are a job roles generator. Given the job requirements, you have to make the list of possible job titles. You can generate upto 5 job titles. Try not to miss small and basic titles. keep it lower cased. include the original job title from user query."""
    return f"Make a list of similar jobroles for the given user query: {user_query}"

def get_job_roles(user_query):
    result = job_roles(user_query)
    return result.content[0].parsed.job_roles

if __name__ == "__main__":
    user_query = "we need a game engine developer in reactjs from a good school"
    print(get_job_roles(user_query))