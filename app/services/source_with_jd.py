from app.services.jobroles import get_job_roles
from app.services.companies import get_companies
from app.services.schools import get_schools, get_school_search_tags

from serpapi import search

from typing import List
from pydantic import BaseModel, Field
import ell
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def scrape_talents_with_jd(job_description, location="Mumbai, India", num_results=20):
    # Your code here
    class GoogleDork(BaseModel):
        dork: str = Field(..., title="Google dork to search for the suitable candidates")

    ell.init()

    @ell.complex(model="gpt-4o", response_format=GoogleDork, temperature=0.5, client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
    def googleDorker(jd: str) -> GoogleDork:
        """You have good knowledge of google dorking. Your aim is to write a google dork to find linkedin profiles having the given specifications. 
        you must include the given tag in every dork`inurl:linkedin.com/in/` to get only the profile links. 
        Write a google dork search query to find linkedin profiles fit for the given job description
        """
        return f"Job Description: {jd}"

    dork = googleDorker(job_description)

    dork = dork.content[0].parsed.dork
    print("="*100)
    print(dork)
    print("="*100)

    print("number of results to give", num_results)
    print(type(num_results))

    results = search(q=dork, engine="google", num=num_results, location=location, api_key=os.getenv("SERPAPI_API_KEY"))

    
    return results['organic_results']



