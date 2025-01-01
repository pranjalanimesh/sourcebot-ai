from typing import List
from pydantic import BaseModel, Field
import ell
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class CompanyModel(BaseModel):
    related_companies: List[str] = Field(..., title="List of related companies")

ell.init()

@ell.complex(model="gpt-4o", response_format=CompanyModel, temperature=0.5, client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
def companies(user_query: str) -> CompanyModel:
    """You have good knowledge of all different types of companies. make a list of all the companies in the given user query. All the company names should be lowercased. You can also return empty list if no information about the companies is found"""
    return f"List different companies for the given user query: {user_query}"

def get_companies(user_query):
    result = companies(user_query)
    return result.content[0].parsed.related_companies

if __name__ == "__main__":
    user_query = "we need a full stack developer in reactjs from a good school and from big tech companies"
    print(get_companies(user_query))