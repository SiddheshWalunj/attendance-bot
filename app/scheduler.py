import random
import time
from app.bot import mark_attendance

def random_delay(min_minutes, max_minutes):
    delay = random.randint(min_minutes * 60, max_minutes * 60)
    time.sleep(delay)

def punch_in():
    random_delay(0, 1)   # 9:15–9:20 handled by cron later
    mark_attendance("in")

def punch_out():
    random_delay(0, 1)  # 8:00–8:30
    mark_attendance("out")
