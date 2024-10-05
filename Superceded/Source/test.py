import requests
from bs4 import BeautifulSoup
import pandas as pd

# The URL for Glassdoor jobs
url = 'https://www.glassdoor.co.in/Job/index.htm'

# Custom headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

# Sending a GET request to the URL with custom headers
response = requests.get(url, headers=headers)

# Checking if the request was successful
if response.status_code == 200:
    # Parsing the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Lists to store scraped data
    job_titles = []
    companies = []
    locations = []

    # Example: Find job titles and company names based on their HTML structure
    jobs = soup.find_all('li', class_='react-job-listing')
    for job in jobs:
        title = job.find('a', class_='jobLink')
        company = job.find('div', class_='jobEmpolyerName')  # Note: Adjust class as per actual HTML

        if title:
            job_titles.append(title.text.strip())
        if company:
            companies.append(company.text.strip())

    # For now, using placeholders for missing data
    locations = ['Location Placeholder'] * len(job_titles)

    # Creating a DataFrame and saving it to CSV
    df = pd.DataFrame({'Job Title': job_titles, 'Company': companies, 'Location': locations})
    df.to_csv('glassdoor_jobs.csv', index=False)

    print("Data scraped and saved to CSV.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
