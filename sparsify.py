# Define a class for boolean formuals
# Implement the tree algorihtms
import csv
import itertools

class k_CNF():
    def __init__(self, file_path=None, clauses=None):
        # XNOR using ==
        if file_path is None == clauses is None:
            raise ValueError("Exactly one of file path or clauses must be specified")

        if clauses is not None:
            self.clauses = clauses
        if file_path is not None:
            self.clauses = set()

            with open(file_path, 'r') as formula_file:
                formula_reader = csv.reader(formula_file)
                for line in formula_reader:
                    clause = frozenset(line)
                    self.clauses.add(clause)

        self.k = max([len(clause) for clause in self.clauses])
        self.literals = set()
        for clause in self.clauses:
            self.literals = self.literals.union(clause)

    def to_csv(self, file_path="output.csv"):
        with open(file_path, 'w', ) as formula_file:
            formula_writer = csv.writer(formula_file)
            for clause in self.clauses:
                formula_writer.writerow(list(clause))

    def get_clauses_at_level(self, level):
        return set(filter(lambda clause: len(clause) == level, self.clauses))

    def theta(self, size, epsilon):
        """ Returns the value of theta for a flower with petals of length 'size'
            for a given epsilon """

        if size <= 0:
            return 2
        else:
            delta = int((self.k ** 2 * 2 ** (2 * self.k + 2)) / (epsilon ** 2)) + 1
            gamma = (4 * delta) ** (2 ** (size - 1) - 1)
            return max(2, gamma * delta)

    def union(self, new_cnf):
        new_clauses = self.clauses.union(new_cnf.clauses)
        return k_CNF(clauses=new_clauses)

    def reduce(self):
        """ Removes all redundant clauses from the formula """
        redundant_clauses = set()
        for C, D in itertools.product(self.clauses, repeat=2):
            if C.issubset(D) and C != D:
                redundant_clauses.add(D)
        self.clauses.difference_update(redundant_clauses)

    def best_flower(self, epsilon):
        """ Returns the best flower in the formula if it exists, -1 otherwise """
        thetas = []
        for level in range(1, self.k + 1):
            thetas.append(self.theta(level - 1, epsilon)) # precompute theta
            for heart_size in range(level, 0, -1):
                clauses_at_level = self.get_clauses_at_level(level)
                for heart in itertools.product(self.literals, repeat=heart_size):
                    heart = frozenset(heart)
                    flower = set()
                    for clause in clauses_at_level:
                        if heart.issubset(clause):
                            flower.add(clause)

                    if len(flower) >= thetas[level - heart_size]:
                        return flower
        return -1

    def __len__(self):
        return len(self.clauses)

    def __repr__(self):
        return "{}-CNF()".format(self.k)

    def __str__(self):
        string_parts = []
        string_parts.append("{}-CNF: \n".format(self.k))
        for clause in self.clauses:
            string_parts.append("{}\n".format(set(clause)))
        return "".join(string_parts)


def sparsify(kcnf, epsilon):
    #print("CNF")
    #print(kcnf)
    best_flower = kcnf.best_flower(epsilon)
    #print("best flower: {}".format(best_flower))
    if best_flower != -1:
        heart = frozenset.intersection(*list(best_flower))
        #print("heart is: {}",format(heart))
        petals = set([clause.difference(heart) for clause in best_flower])
        #print("petals is: {}",format(petals))
        cnf_heart = kcnf.union(k_CNF(clauses=set([heart])))
        cnf_heart.reduce()
        #print("reduced heart: {}".format(cnf_heart))
        cnf_petals = kcnf.union(k_CNF(clauses=petals))
        cnf_petals.reduce()
        #print("reduced petals: {}".format(cnf_petals))
        return sparsify(cnf_heart, epsilon) + sparsify(cnf_petals, epsilon)
    else:
        return [kcnf]
