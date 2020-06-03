import psutil
import time
import datetime

interval = 10 * 60

"""

cpu percent is psutil.cpu_percent()

total memory that exists on computer: psutil.virtual_memory().total

memory percent used is psutil.virtual_memory().percent

"""

def add_checkpoint():
    now = datetime.datetime.today()
    
    year = now.year
    month = now.month
    day = now.day
    
    hour = now.hour
    minute = now.minute

    day = f"{year}-{day}-{month}"
    time = f"{hour}:{minute}"
    
    entry = f"""    time: {day} {time}
    cpu: {psutil.cpu_percent()}
    memoryUsed: {psutil.virtual_memory().percent}
    totalMemory: {psutil.virtual_memory().total}
"""

    f = open("data.txt", 'a')

    f.write(
            "resourceCheck {\n" + entry + "}\n"
            )

    f.close()

while True:
    time.sleep(interval)
    add_checkpoint()
