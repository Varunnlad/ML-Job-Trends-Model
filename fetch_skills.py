import requests
import json
import os
import re
from collections import Counter
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Adzuna API credentials
API_ID = os.getenv("ADZUNA_API_ID")
API_KEY = os.getenv("ADZUNA_API_KEY")
COUNTRY = "in"  # 'in' for India

# Define API Endpoint
URL = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1?app_id={API_ID}&app_key={API_KEY}&results_per_page=50"

# List of skills to track
COMMON_SKILLS = ["Python", "JavaScript", "Machine Learning", "SQL", "React", "AWS", "Data Science", "Docker", "TensorFlow"]

def get_job_data():
    """Fetch job data from Adzuna API."""
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching job data:", response.status_code, response.text)
        return None

def extract_skills(job_data):
    """Extract and count skill occurrences from job descriptions."""
    skill_count = Counter()
    
    for job in job_data.get("results", []):
        description = job.get("description", "").lower()
        
        for skill in COMMON_SKILLS:
            skill_lower = skill.lower().replace(" ", "")  # Handle spaces (e.g., "Machine Learning" -> "machinelearning")
            if skill_lower in description.replace(" ", ""):
                skill_count[skill] += 1

    return dict(skill_count.most_common(5))  # Return top 5 skills

# Fetch job data
job_data = get_job_data()

if job_data:
    # Save raw job data (for debugging)
    with open("job_data.json", "w") as f:
        json.dump(job_data, f, indent=4)

    # Extract top skills
    top_skills = extract_skills(job_data)

    # Save skills data for frontend
    with open("skills.json", "w") as f:
        json.dump({"top_skills": top_skills}, f, indent=4)

    print("Top 5 In-Demand Skills saved in skills.json:", top_skills)
else:
    print("Failed to fetch job data.")
    
