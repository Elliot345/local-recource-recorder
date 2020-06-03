import pygame, time, datetime, sys
pygame.init()

# the function you call to return a list of dicts for data entries (reading data)

def read_data():
    f = open('data.txt', 'r')
    lines = f.readlines()
    f.close()

    # getting data from data.txt ( each entry gets put into a list as a dict (eg. data[entry][object] ) )

    entry = {}

    reading_entry = False

    data = []

    for line in lines:

        # removing \n from line (it's at the end of all lines)

        line = line[:-1]

        # finding out wether to start reading an entry or end it, or reading a line

        if line == 'resourceCheck {':
            reading_entry = True
        elif line[-1:] == '}':
            reading_entry = False
            data.append(entry)
            entry = {}
        elif reading_entry:

            # removing white space

            line = line.split(' ')

            sub_count = 0

            for i in range(len(line)):
                if line[i - sub_count] == '':
                    del line[i - sub_count]
                    sub_count += 1

            # adding split things after : back together

            variable = ""

            for i in line[1:]:
                variable += i
                variable += ' '
            variable = variable[:-1]

            line[1] = variable

            del variable

            sub_count = 0

            for i in range(len(line)):
                if line[i - sub_count] == '':
                    del line[i - sub_count]
                    sub_count += 1
            
            # removing ":" at the end of item name

            line[0] = line[0][:-1]

            # assigning entry data
            
            entry[line[0]] = line[1]

    return data

# the function you run to get the year, day, month, hour, minute, second

def read_time(input_date):

    # getting day and time

    day_time = input_date.split(':')
    day = day_time[0]
    time = day_time[1]

    del day_time

    # reading what day it is

    temp_day = day.split('-')

    # assigning values

    year = temp_day[0]
    day = temp_day[1]
    month = temp_day[2]

    # reading what time it is
    
    # splitting time into list

    temp_time = time.split('-')
    del time

    # assigning values

    hour = temp_time[0]
    minute = temp_time[1]
    second = temp_time[2]

    return {'year': year, 'day': day, 'month': month, 'hour': hour, 'minute': minute, 'second': second}

# the function to show text

def show_text(text, x, y, size, color=(0, 0, 0)):
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)

# a function that returns the date minus a number of time (put in the minus_time as hours)

def find_time(minus_hours):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    hour -= minus_hours + reference['end_time']
    while hour < 1:
        day -= 1
        hour += 24
    while day < 1:
        month -= 1
        day += 30
    while month < 1:
        year -= 1
        month += 12

    hour = round(hour)
    minute = round(minute)
    
    return f'{year}-{day}-{month} {hour}:{minute}'

# the function you run to convert a date to how many minutes ago it was

def convert_to_minutes(input_date):
    
    # converting input date time to date and time

    date_time = input_date.split()

    date = date_time[0].split('-')
    time = date_time[1].split(':')
    
    del date_time

    year = int(date[0]) - 2000
    month = int(date[2])
    day = int(date[1])
    hour = int(time[0])
    minute = int(time[1])

    # calculating time in minutes

    minutes = 0

    month += year * 12
    day += month * 30
    hour += day * 24
    minute += hour * 60
    minutes = minute

    return minute

# showing data

screen = pygame.display.set_mode((1280, 720))

options = ['CPU', 'MEMORY']

selected = 0

reference = {'range_shown': 24, 'end_time': 0}

clock = pygame.time.Clock()

while True:
    current_time = datetime.datetime.now()
    data = read_data()

    screen.fill((255, 255, 255))

    # showing options (eg. CPU, MEMORY, etc.)

    for i in range(len(options)):
        if i == selected:
            pygame.draw.rect(screen, (0, 0, 255), (200 + (i * 200), 50 - 32, 200, 50))
        show_text(options[i], 300 + (i * 200), 50, 32)

    # putting blue on part of the display

    pygame.draw.rect(screen, (0, 0, 255), (0, 66, 1280, 720 - 66))
    
    # displaying reference points

    for i in range(5):
        show_text(find_time(reference['range_shown'] * (i / 5)), 1200 - (250 * i), 75, 16)
        pygame.draw.line(screen, (0, 0, 0), [1200 - (250 * i), 83], [1200 - (250 * i), 720])

    # displaying entries

    # the amount of pixels a minute takes up

    pixels_per_minute = 1000 / (reference['range_shown'] * 60 * 0.8)

    pixels_per_percent = (700 - 83) / 100

    points = []

    current_time = convert_to_minutes(find_time(0))

    itteration = 1

    for entry in data:
        if options[selected] == 'CPU':

            time_from_now = current_time - int(convert_to_minutes(entry['time']))

            x = 1200 - (pixels_per_minute * time_from_now)

            y = 700 - (pixels_per_percent * float(entry['cpu']))

            # adding in points (the first if statement is putting in the bottum as is the last)

            if itteration == 1:
                points.append((x, 700))

            points.append((x, y))

            if itteration == len(data):
                points.append((x, 700))

            itteration += 1

    pygame.draw.polygon(screen, (0, 0, 0), points)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    clock.tick(0.01)
