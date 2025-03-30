# Tank Allocation 

## 数据介绍
以下是 `./data/dataTankAllocation/0000.json` 的部分数据
```json
"volumes": [1861, 2262, 256, 0, 0, 1046, 0, 717, 603, 807, 717, 555, 1672, 1606, 2979], 
"conflicts": [
		[0, 3],[0, 4], [1, 3], [1, 7], [2, 6], [2, 8],[3, 5], [3, 6], [3, 13], [4, 6], [4, 7], [4, 11], [6, 8], [6, 14], [7, 8], [7, 11], [8, 13], [9, 11]], 
"tanks": [
	{
        "capacity": 813, 
        "impossibleCargos": [13], 
        "neighbors": [11, 16, 6, 9, 23, 17]
	},{
        "capacity": 814, 
        "impossibleCargos": [], 
        "neighbors": [6, 20, 14, 13, 18]
	}
]
```
- volumes : 货物的体积
- conflicts : 货物之间的冲突
- tanks 
    - capacity : tank 的容量
    - impossibleCargos : 不能装载的 volumes 序号
    - neighbors : 相邻 tank, 避免出现相邻的 tank 装有存在 conflict 的货物
## 问题限制
- C1: 所有 `volumes` 中的货物必须都被装载到 `tank` 中, 并且 $\sum\limits\text{tank} \geq \text{ volume[i]}$
- C2: `ImpossibleCargos` 的货物不能装载到该 `tank` 中
- C3: 存在 `Conflicts` 的货物不能被装在到相邻的 `tank` 中

## python 代码分析

### 类的参数
```python
self.path # 数据文件的路径
self._content # 所有数据
self._volumes # volumes 信息
self._conflicts # conflicts 信息
self._tanks # tank 信息
```

### 类的函数
```python
get_new_file(new_path) # 清空原数据, 并选择新的数据文件
read_file() # 读取数据, 并将数据放入类的参数
define_vars() # 定义变量
def_sat() # 定义限制
veferication(thesolution) # 验证 该解是否满足容量限制
solve() # 求解
```

### 函数 `define_vars`
定义参数
```python
def define_vars(self):
    global vars
    vars = VarArray(
        size=len(self._tanks), # 参数的数量 = tank 的数量
        dom=range(len(self._volumes) + 1) # 参数的定义域, 存在 volume=0, 因此 可以 + 1, 表示该货物不需要被 tank 装载
    )
```


### 函数 `def_sat`

#### C1: 装载货物 i 的 tank 的总容量大于 volumes[i]
```python
[
    Sum([self._tanks[i]['capacity'] * (vars[i] == t) for i in range(len(self._tanks))]) >= self._volumes[t] 
    for t in range(len(self._volumes)) if self._volumes[t] > 0
],   
```

#### C2: tank i 中不能装载 impossobleCargos 中的货物
```python
[
    vars[i] != cargo
    for i in range(len(self._tanks))
    for cargo in self._tanks[i]['impossibleCargos']
],
```

#### C3: 存在 conflict 的货物不能放在相邻的 tank 中
```python
[
    (vars[i] != x) | (vars[j] != y)
    for (x,y) in self._conflicts
    for i in range(len(self._tanks))
    for j in self._tanks[i]['neighbors']
]
```

### 函数 `verification`

```python
def veferication(self, thesolution):
    # 容量测试
    tank_volumes = [0 for _ in range(len(self._volumes))] # 初始化tank装载量的列表
    for idx, num in enumerate(thesolution):
        tank_volumes[num] += self._tanks[idx]['capacity'] # 将每个装载该序号的 tank 的容量进行求和
    print(tank_volumes) # 显示货物的容量
    print(self._volumes) # 显示装载货物的 tank 的容量
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
```

## 策略对比
| option | time | solved |
|---|---|---|
| FrbaOnDom | 11.97s |Yes |
| FirstFail | 4.77s |No |
| MaxDegree | 4.41s |No |
| MinDomain | 3.72s |No |
| DomOverDeg | 4.18s |No |
| Random | 5.64s |No |
| Min | 3.86s |No |
| Max | 3.88s |No |
| Random | 5.61s |No |
| OccurMost | 3.89s |No |
| OccurLeast | 3.78s |No |
## 遇到的问题
1. 无法在不添加 `options="-varh=FrbaOnDom"` 的情况下找到解
2. 在添加其他 option 之后无法找到解, 但是速度会快于`FrbaOnDom`
3. 对于 `volume=0` 的货物, 应当可以添加一条限制, 但是没能找到有效方法, 因此 `dom=range(len(self._volumes) + 1)` 没有有效利用其中的 `+ 1` 部分

