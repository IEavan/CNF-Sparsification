from gen_cnfs import gen_uniform
import sparsify

cnf = gen_uniform(n=10, m=100)
print("|F| = {}".format(len(cnf)))
result = sparsify.sparsify(cnf, 100)
print("max |F_i| = {}".format(max([len(f) for f in result])))
print("Num formulas: {}".format(len(result)))
