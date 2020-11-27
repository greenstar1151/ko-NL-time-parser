import copy
import inspect
import types
from datetime import datetime, timedelta
from pprint import pprint

from dataset import dataset


class timeObject():
    def __init__(self, exec, meta, name = '') -> None:
        self.exec = exec
        self.frontW = int(meta[0])
        self.backW = int(meta[1])
        self.name = name
    
    def getTotalW(self) -> int:
        return self.frontW * self.backW

    def setW(self, front: int, back: int) -> None:
        self.frontW = front
        self.backW = back

    def __repr__(self) -> str:
        return f'|{self.frontW}|-timeObject({self.name})-|{self.backW}|'
        if type(self.exec) == types.LambdaType:
            l = str(inspect.getsourcelines(self.exec)[0])
            #l = l.split("'exec':")[1].strip()[:-5] # temp
            return f'|{self.frontW}|-timeObject({l})-|{self.backW}|'
        else:
            return f'|{self.frontW}|-timeObject({self.exec})-|{self.backW}|'


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
            string += c
        last_type = c.isdecimal()
    else:
        parsed.append(string)

    for i, tok in enumerate(parsed):
        if type(tok) == str:
            try:
                timeObj = timeObject(dataset[tok]['exec'], dataset[tok]['meta'], tok)
                parsed[i] = timeObj
            except KeyError:
                raise NotImplementedError # TODO: temp
        elif type(tok) == float:
            timeObj = timeObject(tok, (1, 0), str(tok))
            parsed[i] = timeObj
           
    return parsed


def parse_time(text, time_base = datetime.now()):
    '''Main parser function'''
    words = text.split(' ') # Basic tokenizing(whitespace)
    translated = []
    for word in words: # Translate to timeObject
        word_translated = to_time(word)
        translated += word_translated
    #pprint(translated)

    optimized = []
    stack = []
    stack_name = []
    for tObj in translated: # Optimize timeObject [ex] [(1, 0), (0, 0), (0, 1)] -> [(1, 1)]
        #print(f'forloop: {tObj}, {tObj.getTotalW()}')
        
        if tObj.getTotalW() == 1:
            optimized.append(tObj)
        else:
            if len(stack) != 0:
                last = stack.pop()
                if type(last) == timeObject:
                    stack_name.append(tObj.name)
                    stack.append(tObj.exec(last.exec))
                else:
                    stack_name.append(tObj.name)
                    stack.append(timeObject(tObj.exec(last), (1, 1), ' '.join(stack_name)))
            else:
                stack.append(tObj)
                stack_name.append(tObj.name)
    else:
        optimized += stack
    #pprint(optimized)

    for tDelta in optimized:
        time_base = tDelta.exec(time_base)

    return time_base



if __name__ == '__main__':
    text = '내일 자정 1분 전'
    time_base = datetime.now()

    print(f'현재 시각: {time_base}')
    print(f'[In] {text}')

    print(f'[Out] {parse_time(text, time_base)}')
