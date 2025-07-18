import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_jobs():
    headers = {'User-Agent': 'Mozilla/5.0'}
    base_url = "https://www.karkidi.com/Find-Jobs/{}/all/India"
    jobs_list = []

    for page in range(1, 11):  # Scrape 10 pages
        url = base_url.format(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        job_blocks = soup.find_all("div", class_="ads-details")

        for job in job_blocks:
            try:
                title = job.find("h4").get_text(strip=True)
                company = job.find("a", href=lambda x: x and "Employer-Profile" in x).get_text(strip=True)
                location = job.find("p").get_text(strip=True)
                key_skills_tag = job.find("span", string="Key Skills")
                skills = key_skills_tag.find_next("p").get_text(strip=True) if key_skills_tag else ""
                jobs_list.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Skills": skills
                })
            except Exception as e:
                print(f"Parsing error: {e}")
        time.sleep(1)

    df = pd.DataFrame(jobs_list)
    df.to_csv("data/latest_jobs.csv", index=False)
    print("✅ Scraping complete and saved to data/latest_jobs.csv")
