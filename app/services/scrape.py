from app.services.jobroles import get_job_roles

def scrape_talents(job_role, company, education, yoe, loc, additional_prompt, num_results):
    # Your code here
    results = ['talent1', 'talent2', 'talent3']
    
    job_roles = []
    if job_role is not None:
        job_roles = get_job_roles(job_role)

    


    return {
        job_roles: job_roles,

    }



