# OPL - Frequency Allocation

## FAP 问题的限制
- C1: 同一 `Cell` 的不同 `Transmitter` 之间的频率至少相隔 16
- C2: 相邻 `Cell` 之间的不同发射频率至少间隔 `distance[ci][cj]`
- C3: 最小化使用的不同频率的总数, 尽可能减少被分配的唯一频率数量

## OPL 代码分析

```OPL
int nbCells = ...; # Cell 的数量
int nbFreqs = ...; # 可用的 Freq 数量
range Cells 1..nbCells; 
range Freqs 1..nbFreqs; 
int nbTrans[Cells] = ..; # 每个 Cell 的 Transmitter 数量
int distance[Cells, Cells] = ...; # Cell 之间的最小频率间隔

# 定义 Transmitter 类型，包含 Cell 和 Transmitter 的索引
struct TransmitterType {Cells c; int t;};
{TransmitterType} Transmits = {<c,t>| c in Cells & t in 1...nbTrans[c]};
var Freqs freq[Transmits]

solve{
    # C1: 同一 `Cell` 的不同 `Transmitter` 之间的频率至少相隔 16
    forall ( c in Cells & ordered t1, t2 in 1...nbTrans[c])
        abs ( freq[<c, t1>] - freq[<c, t2>]) >= 16;

    # C2: 相邻 `Cell` 之间的不同发射频率至少间隔 `distance[ci][cj]`
    forall ( ordered c1, c2 in Cells: distance[c1, c2] > 0)
        forall ( t1 in 1...nbTrans[c1] & t2 in 1...nbTrans[c2])
            abs ( freq[<c1, t1>] - freq[<c2, t2>]) >= distance[c1,c2];
};

search{
    forall ( t in Transmits ordered by increasing <dsize(freq[t]), nbTrans[t.c]>)
        tryall ( f in Freqs ordered by decreasing nbOccur(f, freq))
            freq[t] = f;
};
```

## Python 代码分析

### 变量
```python 
# 索引
Cells = range(nbCells)
Freqs = range(1, nbFreqs + 1)
Transmits = [(c, t) for c in Cells for t in range(nbTrans[c])]
# 变量
freq = VarArray(size=len(Transmits), dom=Freqs)
```
定义了 freq 变量数组, 其大小为 Transmits 的长度, 每个元素的域为 Freqs, 即 Freq 的取值范围.
每个 `freq[i]` 表示 `Transmitter[i]` 被分配的频率


### 限制
```python
satisfy(
    # C1: 同一 `Cell` 的不同 `Transmitter` 之间的频率至少相隔 16
    [abs(freq[i] - freq[j]) >= 16
     for c in Cells 
     for i, (c1, t1) in enumerate(Transmits) if c1 == c
     for j, (c2, t2) in enumerate(Transmits) if c2 == c and t1 < t2],

    # C2: 相邻 `Cell` 之间的不同发射频率至少间隔 `distance[ci][cj]`
    [abs(freq[i] - freq[j]) >= distance[c1][c2]
     for i, (c1, t1) in enumerate(Transmits)
     for j, (c2, t2) in enumerate(Transmits)
     if c1 < c2 and distance[c1][c2] > 0]
)
# C3: 最小化使用的不同频率的总数
minimize(NValues(freq))
```

## 策略对比
### without minimize
| option | time | solved | 
|---|---|---|
| FrbaOnDom | 5.65s | Yes |
| FirstFail | 3.82s | No |
| MaxDegree | 4.03s | No |
| MinDomain | 5.11s | No |
| DomOverDeg | 4.28s | No |
| Random | 3.79s | No |
| Min | 4.98s | No |
| Max | 4.25s | No |
| Random | 4.07s | No |
| OccurMost | 6.30s | No |
| OccurLeast | 4.00s | No |

### with minimize
| option | time | solved |
|---|---|---|
| FrbaOnDom | +10Mins | No | 
| FirstFail | 4.25 s|No | 
| MaxDegree | 4.10 s|No | 
| MinDomain | 5.32 s|No | 
| DomOverDeg | 4.17 s|No | 
| Random | 4.12 s|No | 
| Min | 5.19 s|No | 
| Max | 4.51 s|No | 
| Random | 4.22 s|No | 
| OccurMost | 5.34 s|No | 
| OccurLeast | 3.95 s|No | 


FrbaOnDom 在十分钟内没有找到解, 在强制停止后返回不加 Minimize 的相同解.


## 遇到的问题
1. 无法解释在不使用 options 或使用 `options="-varh=FrbaOnDom"`的情况下可以找到解, 但是其他的 option 无法找到解. 
2. 在添加 `Minimise` 之后, 不使用 options 或使用 `options="-varh=FrbaOnDom"`的情况下会消耗大量时间, 无法找到解, 而强制停止后返回不加 Minimize 的相同解.
3. 在 (2) 的基础上, 可以观察到, 如果使用`varh`, 那么会需要稍微多一点点的时间显示无解, 但是在使用`valh`时, 则会需要少一点的时间显示无解
