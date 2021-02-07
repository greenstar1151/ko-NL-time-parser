from datetime import datetime, timedelta

from ko_NL_time_parser import parse_time


testcase = [
    {
        'text': '내일 자정 1분 전',
        'time_base': datetime.now()
    },
    {
        'text': '자정 1분 전',
        'time_base': datetime.now()
    },
    {
        'text': '오늘 정오 30분 후',
        'time_base': datetime.now()
    },
    {
        'text': '2시간 후',
        'time_base': datetime.now()
    },
    {
        'text': '30초 후',
        'time_base': datetime.now()
    },
    {
        'text': '1일 2시간 34분 56초 후',
        'time_base': datetime.now()
    },
    {
        'text': '한달 뒤',
        'time_base': datetime.now()
    },
    {
        'text': '일주일 뒤',
        'time_base': datetime.now()
    },
    {
        'text': '한달 일주일 뒤 자정 1시간 30분 전',
        'time_base': datetime.now()
    },
]


for i, case in enumerate(testcase):
    text = case['text']
    time_base = case['time_base']
    print(f'### case {i+1} ###')
    print(f'기준 시각: \t{time_base}')
    print(f'[In] \t\t{text}')
    print(f'[Out] \t\t{parse_time(text, time_base)[0]}')
    print()
