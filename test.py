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

def run_examples(k=3, eps=10, n_max=30, step=1):
    sparsity_results = []
    sparsity_bound = []
    num_formulas = []
    tree_height = []
    num_petal_branches = []
    petal_bounds = []

    delta = int((k ** 2 * 2 ** (2 * k + 2)) / (eps ** 2))

    for n in tqdm(range(max(step, k), n_max + 1, step)):
        cnf = gen_uniform(n=n, k=k, m=5*n)
        required_sparseness = 2 * k * cnf.theta(k-1, eps) * n
        petal_bound = int(n * k / delta) + 1

        tree = sparsify.SparseTree(cnf)
        tree.build_tree(eps)

        max_clauses = max([len(f) for f in tree.get_leaf_formulas()])
        sparsity_results.append(max_clauses)
        sparsity_bound.append(required_sparseness)
        num_formulas.append(tree.num_formulas())
        tree_height.append(tree.height())
        num_petal_branches.append(tree.num_petal_branches())
        petal_bounds.append(petal_bound)

    with open("table_sparsity_{}_{}.csv".format(k ,eps), 'w') as table:
        table_writer = csv.writer(table)
        table_writer.writerow(["k", "epsilon", "n", "achieved_sparsity", "bound",
                               "num_formulas", "tree_height", "num_petal_branches", "petal_bound"])
        for i, n in enumerate(range(max(step, k),n_max + 1,step)):
            table_writer.writerow([k, eps, n, sparsity_results[i],
                                   sparsity_bound[i], num_formulas[i],
                                   tree_height[i], num_petal_branches[i],
                                   petal_bounds[i]])

# TODO Gen example
def example(k=3, n=3, m=9, eps=10):
    cnf = gen_uniform(k=k, n=n, m=m)
    tree = sparsify.SparseTree(cnf)
    tree.build_tree(eps)
    print(tree.to_latex())

if __name__ == "__main__":
    example(n=4, m=5)
    # run_examples(eps=0.01, n_max=15)
    # run_examples(eps=0.1, n_max=15)
    # run_examples(eps=1, n_max=15)
    # run_examples(eps=10, n_max=15)
