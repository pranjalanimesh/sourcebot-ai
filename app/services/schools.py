from typing import List
from pydantic import BaseModel, Field
import ell
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


class SchoolsModel(BaseModel):
    schools: List[str] = Field(..., title="List of Schools")

@ell.complex(model="gpt-4o", response_format=SchoolsModel, temperature=0.5, client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
def schools(user_query: str) -> SchoolsModel:
    """You have good knowledge of different schools and colleges. Given the user query, you have to list a list of similar schools. You can generate upto 5."""
    return f"Given user query: {user_query}"

def get_schools(user_query):
    result = schools(user_query)
    return result.content[0].parsed.schools


@ell.complex(model="gpt-4o", response_format=SchoolsModel, temperature=0.5, client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
def school_search_tags(school_name: str) -> SchoolsModel:
    """You are a school search keyword generator. Given the school name, you have to generate the list of keywords which can be used in google search. You can generate upto 5 short keywords. Try to cover all possible permutations in which the school name is used on linkedin. keep it as short as possible. 
    NOTE: There should be atleast one with only the main school name"""
    return f"Generate search tags for the given school name: {school_name}"

def get_school_search_tags(school_name):
    result = school_search_tags(school_name)
    return result.content[0].parsed.schools


if __name__ == "__main__":
    user_query = "we need a consultant from a good school like stanford"
    schools = get_schools(user_query)

    school_tags = []
    for school in schools:
        print(school)
        school_tags.extend(get_school_search_tags(school))
    
    print(school_tags)

    