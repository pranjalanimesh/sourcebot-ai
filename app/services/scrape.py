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

def scrape_talents(job_role, company, education, yoe, loc, additional_prompt, num_results):
    # Your code here
    
    if additional_prompt is None:
        additional_prompt = ""

    print('Job role:', job_role)
    job_roles = []
    if job_role is not None:
        print('Getting similar jobroles')
        job_roles = get_job_roles(job_role)

    print(job_roles)

    print('Company:', company)
    companies = []
    if company is not None:
        print('Getting similar companies')
        companies = get_companies(company)
    print(companies)


    print('Education:', education)
    schools = []
    if education is not None:
        print('Getting similar schools')
        schools = get_schools(education)
    
    print(schools)

    print("Experience:", yoe)
    experience = []
    if yoe is not None:
        experience.append(yoe)
    
    print(experience)

    print("Location:", loc)
    location = []
    if loc is not None:
        location.append(loc)
    
    print(location)
    class GoogleDork(BaseModel):
        dork: str = Field(..., title="Google dork to search for the suitable candidates")

    ell.init()

    @ell.complex(model="gpt-4o", response_format=GoogleDork, temperature=0.5, client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
    def googleDorker(user_query: str) -> GoogleDork:
        """You have good knowledge of google dorking. Your aim is to write a google dork to find linkedin profiles having the given specifications. 
        you must include the given tag in every dork`inurl:linkedin.com/in/` to get only the profile links. 
        Given below is just an example to search for multiple companies, job roles or schools. The below example is to find candidates from mit or harvard who are software engineers and has 1 or 2 yrs of experience
        EXAMPLE 1: `inurl:linkedin.com/in/ ("MIT" OR "Massachusetts Institute of Technology" OR "Harvard") AND "Software Engineer" AND ("1 yr" OR "2 yrs")`
        DO NOT INCLUDE ANYTHING WHICH IS NOT GIVEN IN USER QUERY.
        """
        return f"Specifications: {user_query}"

    user_query = ''
    if len(job_roles)>0:
        user_query += f"\n job_roles: {' '.join(job_roles)}"
    if len(companies) > 0:
        user_query += f"\n companies: {' '.join(companies)}"
    if len(schools) > 0:
        user_query += f"\n schools: {' '.join(schools)}"
    if len(experience) > 0:
        user_query += f"\n experience in years: {' '.join(experience)}"
    if len(location) > 0:
        user_query += f"\n location: {' '.join(location)}"
    if len(additional_prompt) > 0:
        user_query += f"\n additional information: {additional_prompt}"

    print("="*100)
    print(user_query)
    print("="*100)
    dork = googleDorker(user_query)

    dork = dork.content[0].parsed.dork
    print("="*100)
    print(dork)
    print("="*100)

    print("number of results to give", num_results)
    print(type(num_results))

    try:
        results = search(q=dork, engine="google", num=num_results, api_key=os.getenv("SERPAPI_API_KEY"))
        
        # Check if results is None or empty
        if not results:
            print("No results returned from SerpAPI")
            return []
            
        # Check if organic_results exists in the response
        if 'organic_results' not in results:
            print("No organic_results in SerpAPI response")
            print("Full response:", results)
            return []
            
        return results['organic_results']
        
    except Exception as e:
        print(f"Error during SerpAPI search: {str(e)}")
        print(f"Search query was: {dork}")
        return []



