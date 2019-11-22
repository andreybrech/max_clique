from docplex.mp.model import Model
import copy

class Graph(object):
    def __init__(self):
        self.V = {}

    def add_edge(self, v1, v2):
        """
        add pair of vertexes to V
        add each other to neighbours
        """
        self._add_vertex_to_neighbours(v1, v2)
        self._add_vertex_to_neighbours(v2, v1)
        return

    def _add_vertex_to_neighbours(self, v1, v2):
        # add vertex v2 to neighbours of vertex v1
        if v1 not in self.V:
            self.add_vertex(v1)
        if v2 in self.V[v1]['neighbours']:
            print('vertex already in neighbours')
            return
        self.V[v1]['neighbours'].add(v2)
        return

    def add_vertex(self, v1):
        if v1 in self.V:
            print('vertex already in graph.Vertexes')
            return
        else:
            self.V[v1] = {}
            self.V[v1]['name'] = v1
            self.V[v1]['neighbours'] = set()
            return


def read_dimacs_graph(file_path):
    g = Graph()
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('c'):  # graph description
                print(*line.split()[1:])
            # first line: p name num_of_vertices num_of_edges
            elif line.startswith('p'):
                p, name, vertices_num, edges_num = line.split()
                print('{0} {1} {2}'.format(name, vertices_num, edges_num))
            elif line.startswith('e'):
                _, v1, v2 = line.split()
                g.add_edge(int(v1), int(v2))
            else:
                continue
        return g


def build_problem(g=Graph()):
    mdl = Model(name='max clique')
    x_range = range(len(g.V))

    # decision variables
    x = dict()
    # x = mdl.integer_var_dict(x_range)
    x = mdl.continuous_var_dict(x_range)

    for i in g.V:
        for j in x_range:
            if (j+1 is not i) and (j+1 not in g.V[i]['neighbours']):
                mdl.add_constraint(x[i-1] + x[j] <= 1)

    for i in x_range:
        mdl.add_constraint(x[i] <= 1)
        mdl.add_constraint(x[i] >= 0)

    mdl.maximize(mdl.sum(x[i] for i in x_range))
    return mdl


eps = 1e-5


def log_solution(res):
    print("Objective", res.get_objective_value())
    # print("solution vars:", end=' ')
    # for i, j in res.iter_var_values():
    #     print(i, j, sep=', ', end='; ')
    # print("")


def is_int_solution(sol):
    if sol.get_objective_value() % 1 != 0:
        return False
    for vars in sol.iter_var_values():
        if vars[1] % 1 > eps and abs(vars[1] % 1 - 1) > eps:
            return False
    print("int solution")
    for i, j in sol.iter_var_values():
        print(i, j, sep=', ', end='; ')
    print("")
    return True


class Solver:
    def __init__(self, objective, vars):
        self.upper_bound = objective
        self.vars = vars
        self.current_best = 0

    def search(self, model):
        m = copy.deepcopy(model)
        self.branch_and_bound_search(m)
        return self.current_best, self.vars

    def branch_and_bound_search(self, model):
        s = model.solve(log_output=False)
        # print("number of constraints:", model.number_of_constraints)
        if s is None:
            print("No solution")
            return
        # log_solution(s)
        if s.get_objective_value() < self.current_best:
            return
        if not is_int_solution(s):
            if s.get_objective_value() > self.upper_bound:
                return
            # branching
            # log_solution(s)
            # print("    best known solution:", self.current_best)
            var_dict = tuple()
            branching_var = 0
            for dic in s.iter_var_values():
                if not var_dict:
                    var_dict = dic
                    branching_var = dic[1]
                else:
                    if dic[1] % 1 > eps and 1 - dic[1] % 1 > eps:
                        if dic[1] % 1 > branching_var % 1:
                            var_dict = dic
                            branching_var = dic[1]

            con1 = var_dict[0] <= int(branching_var)
            con2 = var_dict[0] >= (int(branching_var) + 1)
            # print("\nbranching:", var_dict[0], "<=", int(branching_var))
            model.add_constraint(con1)
            self.branch_and_bound_search(model)
            model.remove_constraint(con1)

            # print("\nbranching:", var_dict[0], ">=", int(branching_var) + 1)
            model.add_constraint(con2)
            self.branch_and_bound_search(model)
            model.remove_constraint(con2)
        else:
            # log_solution(s)
            # print("    best known solution:", self.current_best)
            if s.get_objective_value() > self.current_best:
                self.current_best = s.get_objective_value()
                self.vars = s.iter_var_values()
                print("* New best:", self.current_best)
            else:
                print(s.get_objective_value(), "<= current_best(", self.current_best, ")")


if __name__ == '__main__':
    # path_test = 'C125.9.clq.txt'
    path_test = 'test2.txt'
    g = read_dimacs_graph(path_test)
    model = build_problem(g)

    sol = model.solve(log_output=True)
    if sol is not None:
        model.print_solution()

        solver = Solver(sol.get_objective_value(), sol.iter_var_values())
        obj, vars = solver.search(model)

        print("\n------> SOLUTION <------")
        print("Objective:", obj)
        print("Solution vars:")
        for c in vars:
            print(c[0], c[1])
        print("\nBranch-and-Bounded from:")
        model.print_solution()
    else:
        print("Model is infeasible")