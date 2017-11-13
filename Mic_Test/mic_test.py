import numpy as np
import re
import  matplotlib.pyplot as plt

with open("output_1_sec.log") as f:
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

plt.plot(x, y)
plt.show()

x = 2