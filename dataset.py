from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta


def ceil_day(t: datetime) -> datetime:
    return t.replace(day = t.day + 1, hour=0, minute=0, second=0, microsecond=0)

def mid_day(t: datetime) -> datetime:
    return t.replace(day = t.day, hour=12, minute=0, second=0, microsecond=0)

def one_month(t: datetime) -> datetime:
    t = t+relativedelta(months=+1)
    return t


dataset = {
    '오늘': {
        'type': 'independent',
        'exps': lambda t: t + timedelta(0),
        'meta': (1, 1),
        'time_stack': False
    },
    '지금': {
        'type': 'independent',
        'exps': lambda t: t + timedelta(0),
        'meta': (1, 1),
        'time_stack': False
    },
    '내일': {
        'type': 'independent',
        'exps': lambda t: t + timedelta(1),
        'meta': (1, 1),
        'time_stack': False
    },
    '모레': {
        'type': 'independent',
        'exps': lambda t: t + timedelta(2),
        'meta': (1, 1),
        'time_stack': False
    },
    '글피': {
        'type': 'independent',
        'exps': lambda t: t + timedelta(3),
        'meta': (1, 1),
        'time_stack': False
    },
    '사흘': {
        'type': 'independent',
        'exps': lambda t: t + timedelta(3),
        'meta': (1, 1),
        'time_stack': False
    },
    '나흘': {
        'type': 'independent',
        'exps': lambda t: t + timedelta(4),
        'meta': (1, 1),
        'time_stack': False
    },
    '일주일': {
        'type': 'independent',
        'exps': lambda t: t + timedelta(7),
        'meta': (1, 1),
        'time_stack': False
    },
    '한달': {
        'type': 'independent',
        'exps': lambda t: one_month(t),
        'meta': (1, 1),
        'time_stack': False
    },

    '정오': {
        'type': 'independent',
        'exps': lambda t: mid_day(t),
        'meta': (1, 1),
        'time_stack': False
    },
    '자정': {
        'type': 'independent',
        'exps': lambda t: ceil_day(t),
        'meta': (1, 1),
        'time_stack': False
    },

    '초': {
        'type': 'dependent',
        'exps': lambda x: timedelta(0, x),
        'meta': (0, 1),
        'time_stack': True
    },
    '분': {
        'type': 'dependent',
        'exps': lambda x: timedelta(0, 60 * x),
        'meta': (0, 1),
        'time_stack': True
    },
    '시간': {
        'type': 'dependent',
        'exps': lambda x: timedelta(0, 3600 * x),
        'meta': (0, 1),
        'time_stack': True
    },
    '일': {
        'type': 'dependent',
        'exps': lambda x: timedelta(x),
        'meta': (0, 1),
        'time_stack': True
    },
    '주일': {
        'type': 'dependent',
        'exps': lambda x: timedelta(7*x),
        'meta': (0, 1),
        'time_stack': True
    },

    '전': {
        'type': 'dependent',
        'exps': lambda x: (lambda t: t - x),
        'meta': (0, 1),
        'time_stack': False
    },
    '후': {
        'type': 'dependent',
        'exps': lambda x: (lambda t: t + x),
        'meta': (0, 1),
        'time_stack': False
    },
    '뒤': {
        'type': 'dependent',
        'exps': lambda x: (lambda t: t + x),
        'meta': (0, 1),
        'time_stack': False
    }
}
