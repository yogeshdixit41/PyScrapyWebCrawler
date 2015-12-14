from apscheduler.scheduler import Scheduler
import os

#Start the scheduler
sched = Scheduler()
sched.start()

def crawl_website():
    os.system('scrapy crawl timesnews')

#Schedule the job on everyday at 3:45 pm (testing purpose)
sched.add_cron_job(crawl_website, year='*', month='*', day='*', week='*', day_of_week='*', hour='18', minute='24', second='00')


while True:
	pass
    
