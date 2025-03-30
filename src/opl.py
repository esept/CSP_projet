from pycsp3 import *
import json
import shutil

''' ----- Read json data ----- '''
data_path = "./data/OPL.json"

with open(data_path) as json_file:
    content = json.load(json_file)
keys = content.keys()
print(keys)

''' ----- Load data ----- '''

nbCells = content['nbCells']
nbFreqs = content['nbFreqs']
nbTrans = content['nbTrans']
distance = content['distance']

Cells = range(nbCells)
Freqs = range(1, nbFreqs + 1)
Transmits = [(c, t) for c in Cells for t in range(nbTrans[c])]

freq = VarArray(size=len(Transmits), dom=Freqs)

''' ----- define constraints ----- '''
satisfy(
    [abs(freq[i] - freq[j]) >= 16
     for c in Cells 
     for i, (c1, t1) in enumerate(Transmits) if c1 == c
     for j, (c2, t2) in enumerate(Transmits) if c2 == c and t1 < t2],

    [abs(freq[i] - freq[j]) >= distance[c1][c2]
     for i, (c1, t1) in enumerate(Transmits)
     for j, (c2, t2) in enumerate(Transmits)
     if c1 < c2 and distance[c1][c2] > 0]
)

minimize(NValues(freq))
shutil.move("./opl.xml","./docs/xmls/opl.xml")

''' ----- solve probleme ----- '''
start_time = time.time()
if solve(options="-varh=FrbaOnDom") is SAT:
    print(values(freq))
end_time = time.time()  # 记录结束时间
elapsed_time = end_time - start_time  # 计算耗时
print(f"求解耗时: {elapsed_time:.2f}秒")
logfile = [i for i in os.listdir("./") if i.endswith('log')][0]
shutil.move(logfile,f"./docs/logs/{logfile}")


