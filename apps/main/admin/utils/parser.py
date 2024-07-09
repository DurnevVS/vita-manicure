from datetime import datetime

def parse_string(text: str):
    lines = [line[3:] for line in text.split('\n') if line.replace('\r', '')]
    str_dates = [
        f'{date.split(' - ')[0]}T{time}'
        for date in lines for time in date.split(' - ')[1].split(', ')
    ]
    str_dates = [
        f'{date.split('T')[0]}.{datetime.now().year}T{date.split('T')[1]}'for date in str_dates
        if len(date.split('.')) == 2
    ]
    dates = [
        datetime.strptime(date.strip(), '%d.%m.%YT%H:%M')
        for date in str_dates
    ]
    return dates
