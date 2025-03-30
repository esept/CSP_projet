from pycsp3 import *
import os
import json

class TankSolver:
    def __init__(self):
        self.path = None
        self._content = None
        self._volumes = None
        self._conflicts = None
        self._tanks = None

    def get_new_file(self, new_path):
        clear()
        self.path = new_path

    def read_file(self):
        with open(self.path) as f:
            content = json.load(f)
        self._volumes = content['volumes']
        self._conflicts = content['conflicts']
        self._tanks = content['tanks']

    def define_vars(self):
        global vars
        vars = VarArray(
            size=len(self._tanks),
            dom=range(len(self._volumes) + 1)
        )

    def def_sat(self):
        satisfy(
            [
                Sum([self._tanks[i]['capacity'] * (vars[i] == t) for i in range(len(self._tanks))]) >= self._volumes[t] 
                for t in range(len(self._volumes)) if self._volumes[t] > 0
            ],
            [
                vars[i] != cargo
                for i in range(len(self._tanks))
                for cargo in self._tanks[i]['impossibleCargos']
            ],
            [
                (vars[i] != x) | (vars[j] != y)
                for (x,y) in self._conflicts
                for i in range(len(self._tanks))
                for j in self._tanks[i]['neighbors']
            ]
        )

    def show_constraint(self):
        print(posted())

    def show_exp(self):
        print('volumes')
        print(len(self._volumes))
        print('conflict')
        print(len(self._conflicts))
        print('tanks')
        print(len(self._tanks))

    def solve(self):
        if solve(options="-varh=FrbaOnDom") is SAT:
            print("Solution found:")
            print(values(vars))
        else:
            print("No solution found.")

    def veferication(self, thesolution):
        # 容量测试
        tank_volumes = [0 for _ in range(len(self._volumes))]
        for idx, num in enumerate(thesolution):
            tank_volumes[num] += self._tanks[idx]['capacity']
        print(tank_volumes)
        print(self._volumes)
        for i,j in zip(tank_volumes,self._volumes):
            if i < j:
                print(f"volumes {tank_volumes.index(i)} is not enough")
                return 
        print("Volumes Constraint is satisfied")
        # impossibleCargos 测试
        for idx, num in enumerate(thesolution):
            for cargo in self._tanks[idx]['impossibleCargos']:
                if num == cargo:
                    print(f"tank {idx} has cargo {cargo} which is impossible")
                    return 
        print("impossibleCargos Constraint is satisfied")
        # conflict 测试
        for idx, num in enumerate(thesolution):
            for neighbor in self._tanks[idx]['neighbors']:
                neighbor_num = thesolution[neighbor]
                # 检查是否存在(num, neighbor_num)或(neighbor_num, num)在conflicts列表中
                if (num, neighbor_num) in self._conflicts or (neighbor_num, num) in self._conflicts:
                    print(f"Conflict found: tank {idx}(cargo {num}) and tank {neighbor}(cargo {neighbor_num})")
                    return 
                    break
        print("Conflict Constraint is satisfied")
        
