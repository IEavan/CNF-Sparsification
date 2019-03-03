import csv
import numpy as np
from sparsify import k_CNF

def gen_uniform(k=3, n=10, m=100):
    variables = np.arange(10) + 1
    literals = np.concatenate((variables, variables * -1))

    clauses = set()
    for i in range(m):
        while True:
            clause = frozenset(np.random.choice(literals, size=k, replace=False))
            if not clause in clauses:
                break
        clauses.add(clause)

    return k_CNF(clauses=clauses)
