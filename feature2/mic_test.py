import numpy as np
import re
import os

def Audio_Check():
    with open("output.log") as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    content = [string.split("'")[1] for string in content]
    content = [re.findall(r'[0-9A-F]+', line, re.I) for line in content]

    y = []
    for line in content:
        for ele in line:
            y.append(int(ele, 16))
    print(y)

    x = []
    for i in range(0, len(y)):
        x.append((1/44100)*i)


    sum = 0;
    audio_raise = 0;

    for i in range(0,len(y)):
        sum = sum + x[i]
    sum = sum / len(y)

    if sum > 2 and sum < 3:
        audio_raise = 1;
    elif sum > 3 and sum < 4:
        audio_raise = 2;
    elif sum > 4:
        audio_raise = 3;
    else:
        audio_raise = 0;
    return (audio_raise)
    
    