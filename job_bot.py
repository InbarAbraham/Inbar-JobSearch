import requests
from bs4 import BeautifulSoup
import telegram
import time

# Telegram settings
TELEGRAM_TOKEN = '8390239033:AAFB9RrLYxLuuMBUewzvviMcE_JOvtz2J7A'
CHAT_ID = '5477799468'
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# List of jobs that were already sent
sent_jobs = set()

# Search keywords
keywords = ["junior", "intern", "student", "ללא ניסיון"]
regions = ["מרכז", "השרון"]

# Function to fetch jobs from AllJobs
def fetch_alljobs():
    results = []
    for keyword in keywords:
        search_url = f'https://www.alljobs.co.il/SearchResultsGuest.aspx?page=1&position=&type=&freetxt={keyword}&city=&region='
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_divs = soup.find_all('div', class_='sum')

        for div in job_divs:
            title_tag = div.find('a', class_='GARegular')
            if title_tag:
                title = title_tag.text.strip()
                link = 'https://www.alljobs.co.il' + title_tag['href']
                desc_div = div.find_next('div', class_='comp')
                location_text = desc_div.text.strip() if desc_div else ""

                if link not in sent_jobs:
                    if any(region in location_text for region in regions):
                        sent_jobs.add(link)
                        results.append((title, link, location_text))
    return results

# Send new jobs via Telegram
def send_jobs(jobs):
    for title, link, location in jobs:
        message = f"📢 New job found:\n*{title}*\n📍 Location: {location}\n🔗 {link}"
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

# Run every 10 minutes
def run_every_10_minutes():
    while True:
        print("🔍 Searching for new jobs...")
        jobs = fetch_alljobs()
        if jobs:
            send_jobs(jobs)
        else:
            print("❌ No new jobs found.")
        time.sleep(600)  # 10 minutes

if __name__ == '__main__':
    run_every_10_minutes()
