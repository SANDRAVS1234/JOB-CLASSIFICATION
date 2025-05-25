from apscheduler.schedulers.blocking import BlockingScheduler
from scraper.job_scraper import scrape_jobs

scheduler = BlockingScheduler()
scheduler.add_job(scrape_jobs, 'interval', hours=24)
scheduler.start()