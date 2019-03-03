from gen_cnfs import gen_uniform
import sparsify
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import csv

def test_simple(n=5, m=25, eps=10):
    cnf = gen_uniform(n=n, m=m)
    print("|F| = {}".format(len(cnf)))
    print("Thetas: {}".format([cnf.theta(i, eps) for i in range(cnf.k)]))

    tree = sparsify.SparseTree(cnf)
    tree.build_tree(eps)
    print("max |F_i| = {}".format(max([len(f) for f in tree.get_leaf_formulas()])))
    print("Num formulas: {}".format(tree.num_formulas()))

def run_examples(k=3, eps=10, n_max=30, step=5):
    sparsity_results = []
    sparsity_bound = []
    sparsity_ratio = []
    num_formulas = []
    for n in tqdm(range(step, n_max + 1, step)):
        cnf = gen_uniform(n=n, k=k, m=5*n)
        required_sparseness = 2 * k * cnf.theta(k-1, eps) * n
        result = sparsify.sparsify(cnf, eps)
        max_clauses = max([len(f) for f in result])
        sparsity_results.append(max_clauses)
        sparsity_bound.append(required_sparseness)
        sparsity_ratio.append(max_clauses / required_sparseness)
        num_formulas.append(len(result))
    with open("table_sparsity_{}_{}.csv".format(k ,eps), 'w') as table:
        table_writer = csv.writer(table)
        table_writer.writerow(["k", "epsilon", "n", "achieved_sparsity", "bound",
                               "ratio", "num_formulas"])
        for i, n in enumerate(range(step,n_max + 1,step)):
            table_writer.writerow([k, eps, n, sparsity_results[i],
                                   sparsity_bound[i], sparsity_ratio[i], num_formulas[i]])

# TODO Tree Height / num petal branches
# TODO Gen example

if __name__ == "__main__":
    test_simple()
    # run_examples(eps=0.01, n_max=100)
    # run_examples(eps=0.1, n_max=100)
    # run_examples(eps=1, n_max=100)
    # run_examples(eps=10, n_max=100)
