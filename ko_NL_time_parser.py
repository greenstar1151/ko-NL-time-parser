import inspect
import types
from datetime import datetime, timedelta
from pprint import pprint

try:
    from .dataset import dataset
except ImportError:
    from dataset import dataset

debug = False

class timeObject():
    def __init__(self, expression, meta, time_stack, name = '') -> None:
        self.expression = expression
        self.frontW = int(meta[0])
        self.backW = int(meta[1])
        self.time_stack = time_stack
        self.name = name
    
    def getTotalW(self) -> int:
        return self.frontW * self.backW

    def setW(self, front: int, back: int) -> None:
        self.frontW = front
        self.backW = back

    def __repr__(self) -> str:
        return f'|{self.frontW}|-timeObject({self.name})-|{self.backW}|'


def to_time(token: str) -> list:
    '''Translates given string to timeObject(s).'''
    parsed = []
    string = ''
    last_type = token[0].isdecimal()
    for c in token:
        if last_type != c.isdecimal():
            try:
                string = float(string)
                parsed.append(string)
                string = c
            except ValueError:
                pass
        else:
            string = str(string) + c
        last_type = c.isdecimal()
    else:
        parsed.append(string)

    for i, tok in enumerate(parsed):
        if type(tok) == str:
            try:
                timeObj = timeObject(dataset[tok]['exps'], dataset[tok]['meta'], dataset[tok]['time_stack'], tok)
                parsed[i] = timeObj
            except KeyError:
                parsed[i] = None
                continue
                raise NotImplementedError # TODO: temp
        elif type(tok) == float:
            timeObj = timeObject(tok, (1, 0), True, str(tok))
            parsed[i] = timeObj
    
    parsed = list(filter(lambda x: x != None, parsed))
    return parsed


def parse_time(text, time_base = datetime.now()):
    '''Parse korean NL time expression to datetime'''
    words = text.split(' ') # Basic tokenizing(whitespace)
    words = filter(lambda x: len(x) > 0, words)
    translated = []
    for word in words: # Translate to timeObject
        word_translated = to_time(word)
        translated += word_translated
    if debug: pprint(translated)

    optimized = []
    stack = []
    stack_name = []
    stack_time = []
    for i in range(len(translated) - 1):
        currObj = translated[i]
        nextObj = translated[i + 1]
        if currObj.getTotalW() == 1:
            optimized.append(currObj)
            continue
        if currObj.backW + nextObj.frontW == 0:
            name = f'{currObj.name}{nextObj.name}'
            newObj = timeObject(nextObj.expression(currObj.expression), 
                                (1, 1), 
                                currObj.time_stack and nextObj.time_stack,
                                name)
            stack_time.append(newObj)
            stack_name.append(name)
        elif nextObj.frontW == 0:
            stack.append(nextObj)
    else:
        if len(translated) > 0:
            if translated[-1].getTotalW() == 1:
                optimized.append(translated[-1])
    
    timeDeltaSum = timedelta(0)
    while len(stack_time) != 0:
        tObj = stack_time.pop()
        timeDeltaSum += tObj.expression
    
    if len(stack) == 1:
        tAlter = stack.pop()
        tAlter.expression(timeDeltaSum)
        tObj = timeObject(tAlter.expression(timeDeltaSum),
                          (1, 1),
                          False,
                          ' '.join(stack_name + [tAlter.name]))
        optimized.append(tObj)

    # for tObj in translated: # Optimize timeObject [ex] [(1, 0), (0, 0), (0, 1)] -> [(1, 1)]
    #     print(f'forloop: {tObj}, {tObj.getTotalW()}')
        
    #     if tObj.getTotalW() == 1:
    #         optimized.append(tObj)
    #     else:
    #         if len(stack) != 0:
    #             last = stack.pop()
    #             stack_name.append(tObj.name)
    #             stack.append(timeObject(tObj.expression(last), (1, 1), ' '.join(stack_name)))
    #             # if type(last) == timeObject:
    #             #     stack_name.append(tObj.name)
    #             #     stack.append(tObj.expression(last.expression))
    #             # else:
    #             #     stack_name.append(tObj.name)
    #             #     stack.append(timeObject(tObj.expression(last), (1, 1), ' '.join(stack_name)))
    #         else:
    #             stack.append(tObj)
    #             stack_name.append(tObj.name)
    # else:
    #     optimized += stack
    if debug: pprint(optimized)

    for tDelta in optimized:
        time_base = tDelta.expression(time_base)

    return time_base, translated, optimized



if __name__ == '__main__':
    debug = True

    text = '1시간 23분 45초 후'
    time_base = datetime.now()

    print(f'현재 시각: {time_base}')
    print(f'[In] {text}')

    print(f'[Out] {parse_time(text, time_base)[0]}')
