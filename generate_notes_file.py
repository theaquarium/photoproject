import datetime
from utils import *
from config import config

start_date = datetime.datetime(2025, 1, 1)
end_date = datetime.datetime(2026, 1, 1)

output = ''

for day in daterange(start_date, end_date):
    dayname = day.strftime("%Y-%m-%d")
    output += dayname + ': ""\n'

with open("notes.yaml", "w") as text_file:
    text_file.write(output)
