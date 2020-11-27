from datetime import timedelta, datetime


def ceil_day(t: datetime) -> datetime:
    return t.replace(day = t.day + 1, hour=0, minute=0, second=0, microsecond=0)

def mid_day(t: datetime) -> datetime:
    return t.replace(day = t.day, hour=12, minute=0, second=0, microsecond=0)


dataset = {
    '오늘': {
        'type': 'independent',
        'exec': lambda t: t + timedelta(0),
        'meta': (1, 1)
    },
    '내일': {
        'type': 'independent',
        'exec': lambda t: t + timedelta(1),
        'meta': (1, 1)
    },
    '정오': {
        'type': 'independent',
        'exec': lambda t: mid_day(t),
        'meta': (1, 1)
    },
    '자정': {
        'type': 'independent',
        'exec': lambda t: ceil_day(t),
        'meta': (1, 1)
    },\
    '초': {
        'type': 'dependent',
        'exec': lambda x: timedelta(0, x),
        'meta': (0, 0)
    },
    '분': {
        'type': 'dependent',
        'exec': lambda x: timedelta(0, 60 * x),
        'meta': (0, 0)
    },
    '시간': {
        'type': 'dependent',
        'exec': lambda x: timedelta(0, 3600 * x),
        'meta': (0, 0)
    },
    '일': {
        'type': 'dependent',
        'exec': lambda x: timedelta(x),
        'meta': (0, 0)
    },
    '전': {
        'type': 'dependent',
        'exec': lambda x: (lambda t: t - x),
        'meta': (0, 1)
    },
    '후': {
        'type': 'dependent',
        'exec': lambda x: (lambda t: t + x),
        'meta': (0, 1)
    }
}