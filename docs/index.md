# pqlattice


## Quick Example

```python
import pqlattice as pq

B = pq.random.randlattice(20, seed=0)
pq.show(B, max_rows=4, max_cols = 6)
```
```
Matrix of integers with shape: 20 x 20
======================================
          [0]      [1]      [2]  ...      [17]      [18]      [19]
 [0]        0   744754   864912  ...   -518094  -1059265  -2020217
 [1]        0  4468524  5208149  ...  15148796   7154090   -905760
 ...      ...      ...      ...  ...       ...       ...       ...
[18]  1485231  1016267  -566813  ...   6150781   7321489   6305462
[19]        0  -744754  -864912  ...  -1587933   -306240   1026485
```
```python
print(pq.lattice.hadamard_ratio(B)) # 0.014816328763771074
min_v = (min(pq.linalg.norm(v) for v in B))
print(min_v) # 2569945.025682845

L = pq.lattice.lll(B)
print(pq.linalg.norm(L[0])) # 87588.95332175172
print(pq.lattice.hadamard_ratio(L)) # 0.8653657544560275

sv = pq.lattice.shortest_vector(L)
print(pq.linalg.norm(sv)) # 87588.95332175172

H = pq.lattice.hkz(L)
print(pq.lattice.hadamard_ratio(H)) # 0.8661175966425156
```
