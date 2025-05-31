import pandas as pd
import requests
import logging
from datetime import datetime
import json
import re
from bs4 import BeautifulSoup
import openai

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools


def clean_html_content(html_content):
    """
    Clean HTML content and extract meaningful text
    """
    try:
        # First use BeautifulSoup to clean basic HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text and clean up whitespace
        text = soup.get_text(separator=' ')
        text = re.sub(r'\s+', ' ', text).strip()
        
        try:
            
            job_description_analyzer = Agent(
            name="Job Description Analyzer",
            role="Analyze and extract key information from job descriptions.",
            model=OpenAIChat("gpt-4.1-nano"),
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "Do not invent any information not present in the original text.",
                f"""
                Clean and structure the following job description text, removing any remaining HTML artifacts or unwanted formatting.
                Organize it into clear sections if possible (e.g., About, Responsibilities, Requirements, Benefits).
                Keep only the essential information and format it in a clean, readable way.
                

                Text to clean:
                {text}
                """
            ],
            markdown=True,
            )

            query = "Analyze and structure this job description: "
            response = job_description_analyzer.run(query)
            job_description_analyzer.print_response(response.content)

            # Process the output
            #cleaned_text = json.loads(response.content.strip())
            cleaned_text = response.content
            
            return cleaned_text
        
        except Exception as e:
            logger.warning(f"GPT cleaning failed, falling back to basic cleaning: {str(e)}")
            return text
            
    except Exception as e:
        logger.error(f"Error cleaning HTML content: {str(e)}")
        return html_content

def get_jobs_from_remotive(category=None, search=None, limit=None):
    """
    Get jobs from Remotive API
    """
    base_url = "https://remotive.com/api/remote-jobs"
    params = {}
    
    if category:
        params['category'] = category
    if search:
        params['search'] = search
    if limit:
        params['limit'] = limit
        
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('jobs', [])
    except Exception as e:
        logger.error(f"Error fetching jobs from Remotive API: {str(e)}")
        return []

def process_jobs(jobs_data):
    """
    Process jobs data and extract relevant information
    """
    processed_jobs = []
    
    for job in jobs_data:
        # Clean the description
        #cleaned_description = clean_html_content(job.get('description', ''))
        
        # Create job entry
        job_info = {
            'Title': job.get('title', ''),
            'Company': job.get('company_name', ''),
            'Location': job.get('candidate_required_location', ''),
            'Description': job.get('description', ''),
            'Posted': job.get('publication_date', ''),
            'Job_Type': job.get('job_type', ''),
            'Apply_Source': 'Remotive',
            'Apply_URL': job.get('url', ''),
            'Via': 'Remotive.com',
            'Qualifications': '',  # Remotive API doesn't provide this directly
            'Salary': job.get('salary', '')
        }
        
        processed_jobs.append(job_info)
    
    return processed_jobs

def main():
    try:
        # Get jobs from Remotive API
        logger.info("Fetching jobs from Remotive API...")
        jobs_data = get_jobs_from_remotive(search="Data Analyst",limit=25)
        logger.info(f"Found {len(jobs_data)} jobs")
        
        # Save raw data
        """
        with open('raw_remotive_jobs_data.json', 'w', encoding='utf-8') as f:
            json.dump(jobs_data, f, indent=2, ensure_ascii=False)
        logger.info("Saved raw jobs data to raw_remotive_jobs_data.json")
        """
        # Process jobs
        processed_jobs = process_jobs(jobs_data)
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(processed_jobs)
        df["Combined"] = (
            "title: " + df["Title"].astype(str) + "\n"
            + "company: " + df["Company"].astype(str) + "\n"
            + "location: " + df["Location"].astype(str) + "\n"
            + "description: " + df["Description"].astype(str)
        )
        df["Coverletter"] = None
        df["recruiter_email"] = None
        df["score"] = None
        df["reason"] = None
        df["status"] = "Not Applied"
        
        # Save to CSV
        df.to_csv('JobsData.csv', index=False, encoding='utf-8')
        logger.info(f"Successfully saved {len(df)} jobs to JobsData.csv")
        
        # Display summary
        print("\nSummary:")
        print(f"Total jobs processed: {len(df)}")
        print(f"Unique companies: {df['Company'].nunique()}")
        print(f"Locations: {df['Location'].unique()}")
        print("\nApplication sources distribution:")
        print(df['Apply_Source'].value_counts())
        #print(df.head(3))
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 





import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs
import pandas as pd
from urllib.parse import urlparse


def get_apply_url(job_listing_url):
    response = requests.get(job_listing_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <a> tag with the button text
    apply_link = soup.find('a', string=lambda s: s and 'Apply for this position' in s)
    
    # If not found, try by class (update class name if needed)
    if not apply_link:
        apply_link = soup.find('a', class_='tw-btn-primary')
    
    if apply_link and apply_link.has_attr('href'):
        return apply_link['href']
    else:
        return None


# Function to extract main job platform (domain without subdomains and TLDs)
def extract_job_platform(url):
    parsed = urlparse(url)
    domain_parts = parsed.netloc.split('.')

    # Remove 'www' or common subdomain prefixes
    domain_parts = [part for part in domain_parts if part not in ['www', 'jobs', 'job-boards', 'boards']]

    # Take the second-level domain (like 'lever' in 'jobs.lever.co')
    if len(domain_parts) >= 2:
        return domain_parts[-2]  # second last part
    elif domain_parts:
        return domain_parts[0]  # fallback
    else:
        return None

# Example: load your DataFrame (update this line with your actual data source)
df = pd.read_csv("JobsData.csv")
df["Apply_URL"] = df["Apply_URL"].apply(get_apply_url)

# Apply function to create 'via' column
df['Apply_Source'] = df['Apply_URL'].apply(extract_job_platform)

#print(df['Apply_URL'])
#print(df['Apply_Source'])

df = df[df['Apply_Source'] != 'greenhouse']

# Step 2: Define custom sort order
priority = ['ashbyhq', 'workable']

# filter jobs
df = df[df['Apply_Source'] == 'ashbyhq'].head(1)

print("Total jobs: "+str(len(df)))

df["Description"] = df["Description"].apply(clean_html_content)

df["Combined"] = (
            "title: " + df["Title"].astype(str) + "\n"
            + "company: " + df["Company"].astype(str) + "\n"
            + "location: " + df["Location"].astype(str) + "\n"
            + "description: " + df["Description"].astype(str)
        )


# Function to assign sort key
def sort_key(x):
    if x in priority:
        return (priority.index(x), x)
    else:
        return (len(priority), x)  # all others go after

# Step 3: Sort the filtered list using the custom key
df = df.sort_values(by='Apply_Source', key=lambda col: col.map(sort_key))

# Reset index if needed
df = df.reset_index(drop=True)
# Save the updated DataFrame
df.to_csv("JobsData.csv", index=False)
