# pqlattice - Python library for lattice based cryptography and cryptoanalysis
## Summary
`pqlattice` is a Python library for **Lattice-based cryptography and cryptoanalysis**.
It provides implmenetations of lattice reduction algorithms such as **LLL**, **BKZ** and **HKZ**, arithemtics over integer quotient rings and polynomial quotient rings and linear algebra functions for integer based matrices.
It also implements discrete guassian distribution and LWE distribution.
Check out the [API reference](https://mikolajlh.github.io/pqlattice/) for full list of modules and functions.

The core version of pqlattice was written in pure python with `numpy` as only dependency.
There is optional dependencies group `pqlattice[fast]`, that uses `fpylll` for lattice reductions and `python-flint` for hermite normal form computations.

## Instalation
For standard version, install directly via pip:
```
pip install pqlattice
```

For fast backend based on fpylll and python-flint:
```
pip install "pqlattice[fast]"
```
Due to fpylll depending on external binaries it might be not trival to install this version of library, especially on windows. We encourage to the users to use google-collab enviroment which already has all external libraries installed and simple `pip install "pqlattice[fast]"` should work.

## Examples
Too see more examples check out the [examples]() page.
### Primary attack against LWE instance
```python
import pqlattice as pq
import numpy as np
import math
pq.settings.set_backend("fast")

n = 14
sigma = 2
q = 1000
m = 50
secret_dist = "ternary"

lwe = pq.random.LWE(n, q, sigma, secret_dist, 80)
secret = lwe.secret
A, b = lwe.sample_matrix(m)

K = pq.lattice.embeddings.kannan(A, b, q)

L = pq.lattice.lll(K)
B = pq.lattice.bkz(L)

short_vector = B[0]
e = v[:m]
s = v[m:m + n]

assert np.all(lwe.secret == s)
```
