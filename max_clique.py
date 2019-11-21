

class Graph(object):
    """
    class of graph
    """
    
    def __init__(self):
        """
        V- множество вершин
        D - множество вершин, с возможностью их сортировки по степени
        colors - нужен только для покраски по вершинам
        """
        self.V = {}
        self.D = [] 
        self._D_sorted = False
        self.used_colors = set()
        self.coloring = dict()

    def add_edge(self,v1,v2):
        """
        add pair of vertexes to V
        add each other to neigbours
        """
        self._add_vertex_to_neighbours(v1,v2)
        self._add_vertex_to_neighbours(v2,v1)
        
        return
    
    def add_vertex(self,v1):
        """
        add one vertex to V
        """
        
        if v1 in self.V: # если вершина есть в множестве, то все ок. Ее не надо добавлять
                         # МБ надо обновить ее степень?
#             v1.update_degree = len(self.neighbours(v1))
#             self.V[v1]['degree'] = self.degree(v1)
#             D[self.V[v1]['D_index'] ] = self.V[v1]['degree']
            print('vertex already in graph.Vertexes')
            
            return
        else:
            self.V[v1] = {}
            self.V[v1]['name'] = v1
            self.V[v1]['neighbours'] = set()
            self.V[v1]['degree'] = 0
#             self.V[v1]['degree_position'] = 0
            self.D.append(self.V[v1])
#             self.V[v1]['D_index'] = len(self.D) - 1
            self._D_sorted = False
#             self.V[v1]['color'] = None
#             self.V[v1]['neigbour_colors'] = set()
            
            return
    
            
    def _add_vertex_to_neighbours(self,v1, v2):
        """
        add vertex v2 to neigbours of vertex v1
        """
        if v1 not in self.V:
            self.add_vertex(v1)
        if v2 in self.V[v1]['neighbours']:
            print('vertex already in neighbours')
            return
        self.V[v1]['neighbours'].add(v2)
        self.V[v1]['degree'] += 1
        self._D_sorted = False

        return
    
    def neighbours(self,v1):
        """
        print all neigbour names of chosed vertex
        """
        if v1 in self.V:
            return self.V[v1]['neighbours']
        else:
            print("no such vertex in graph")
            return None 
        
    def is_neighbour(self,vertex_name,neighbour_name):
        """
        vetrex - vertex name
        neighbout - neighbour name
        True if neighbour
        False if not neighbour
        """
        if neighbour_name in self.V[vertex_name]['neighbours']:
            return True
        return False
    
    
        
    def sort_vertex_by_degree(self):
        """
        sort vertexes: big degree is first
        """
        # добавить маркер сортер для массива Д для того, чтобы не сортировать сортированный Д
        if self._D_sorted :
            return
        self.D.sort(key= lambda input: input['degree'])
        self._D_sorted = True
        return

    def degree(self,v1):
        """
        return degree of chosen vertex
        """
        if v1 in self.V:
            return len(self.V[v1]['neighbours'])
        else:
            return None
        
    def neighbour_max_degree(self,v1):
        """
        if vertex have neighbours - return neighbour with maximum degree
        if vertex don't have neighbours - return None
        """
        if len ( self.V[v1]['neighbours'] ) == 0:
            return None
        neighbour_max_degree_name = self.V[v1]['neighbours'].pop() # random vervex from neighbours 
        self.V[v1]['neighbours'].union(self.V[v1]['neighbours'], {neighbour_max_degree_name}) #back poped vertex back to neighbours
        max_degree = self.V[neighbour_max_degree_name]['degree']
            
        for neighbour in self.V[v1]['neighbours']:
            if self.V[neighbour]['degree'] > max_degree:
                max_degree = self.V[neighbour]['degree']
                neighbour_max_degree = self.V[neighbour]
        return neighbour_max_degree
    
    def vertex_max_degree(self):
        self.sort_vertex_by_degree()
        return self.D[0]
    
    def clear_coloring(self):
        self.used_colors = set()
        self.coloring = dict()

        
    def recolor(self):
        """
        Использовать с candidates при ветвлении
        т.к в первоначальной окраске слишком много цветов
        скорее всего стоит красить не каждое ветвление, а мб только в начале
        """
        max_color = -1
        self.coloring = dict()
        for vertex_name in self.V:
            self.coloring[vertex_name] = None
        self.used_colors = dict()
        for vertex_name in self.V:
            avalible_colors = set(self.used_colors.keys() )
            for neighbour_name in g.V[vertex_name]['neighbours']:
                avalible_colors -= {self.coloring[neighbour_name]}
                if len( avalible_colors ) == 0:
                    break
            if len( avalible_colors ) == 0:
                max_color += 1 # color is index in candidates_coloring
                self.used_colors[max_color] = set()
                self.used_colors[max_color].add(vertex_name)
                self.coloring[vertex_name] = max_color

            if len( avalible_colors ) != 0:
                for avalible_color in avalible_colors:
                    rand_avalible_color = avalible_color
                    break
                self.used_colors[rand_avalible_color].add(vertex_name)
                self.coloring[vertex_name] = rand_avalible_color

    def recolor_by_degree(self):
        """
        Использовать с candidates при ветвлении
        т.к в первоначальной окраске слишком много цветов
        скорее всего стоит красить не каждое ветвление, а мб только в начале
        """
        self.sort_vertex_by_degree()
        max_color = -1
        self.coloring = dict()
        for vertex_name in self.V:
            self.coloring[vertex_name] = None
        self.used_colors = dict()
        for vertex in self.D:
            vertex_name = vertex['name']
            avalible_colors = set(self.used_colors.keys() )
            for neighbour_name in g.V[vertex_name]['neighbours']:
                avalible_colors -= {self.coloring[neighbour_name]}
                if len( avalible_colors ) == 0:
                    break
            if len( avalible_colors ) == 0:
                max_color += 1 # color is index in candidates_coloring
                self.used_colors[max_color] = set()
                self.used_colors[max_color].add(vertex_name)
                self.coloring[vertex_name] = max_color

            if len( avalible_colors ) != 0:
                for avalible_color in avalible_colors:
                    rand_avalible_color = avalible_color
                    break
                self.used_colors[rand_avalible_color].add(vertex_name)
                self.coloring[vertex_name] = rand_avalible_color

    def recolor_by_degree_reverse(self):
            """
            Использовать с candidates при ветвлении
            т.к в первоначальной окраске слишком много цветов
            скорее всего стоит красить не каждое ветвление, а мб только в начале
            """
            self.sort_vertex_by_degree()
            max_color = -1
            self.coloring = dict()
            for vertex_name in self.V:
                self.coloring[vertex_name] = None
            self.used_colors = dict()
            for vertex_index in range(len(self.D)-1,-1,-1):
                vertex = self.D[vertex_index]
                vertex_name = vertex['name']
    #             print('vertex_name',vertex_name)
    #             print('used_Colors',self.used_colors)
                avalible_colors = set(self.used_colors.keys() )
                for neighbour_name in g.V[vertex_name]['neighbours']:
    #                 print('N',neighbour_name, self.coloring[neighbour_name] ,)
                    avalible_colors -= {self.coloring[neighbour_name]}
                    if len( avalible_colors ) == 0:
                        break
                if len( avalible_colors ) == 0:
                    max_color += 1 # color is index in candidates_coloring
                    self.used_colors[max_color] = set()
                    self.used_colors[max_color].add(vertex_name)
                    self.coloring[vertex_name] = max_color

    #             print('avalible_colors',avalible_colors)
                if len( avalible_colors ) != 0:
                    for avalible_color in avalible_colors:
                        rand_avalible_color = avalible_color
                        break
                    self.used_colors[rand_avalible_color].add(vertex_name)
                    self.coloring[vertex_name] = rand_avalible_color
    #             print('chosen_Color',self.coloring[vertex_name])


def read_dimacs_graph(file_path):
    '''
        Parse .col file and return graph object
    '''
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
                g.add_edge(v1,v2)
            else:
                continue
        return g


def initial_heuristic_degree_2():
    clique = set()
    g.sort_vertex_by_degree()
#     print(type(clique))
    for vertex in g.D:
#         print(type(clique),type(vertex))
        
        all_elements_in_clique_are_neighbours_to_vertex = True
        for element in clique:
            all_elements_in_clique_are_neighbours_to_vertex = all_elements_in_clique_are_neighbours_to_vertex and g.is_neighbour(vertex['name'],element)
            if not all_elements_in_clique_are_neighbours_to_vertex:
                break
#         print(vertex['name'],all_elements_in_clique_are_neighbours_to_vertex )
        if all_elements_in_clique_are_neighbours_to_vertex:
            clique.add(vertex['name'])
    return clique



def initial_heuristic_color():
    """
    makes clique:
    first - vericies with maximal color
    """
    clique = set()
    g.sort_vertex_by_degree()
    
    for color in range(len(g.used_colors)):
        for vertex_name in g.used_colors[color]:
            all_elements_in_clique_are_neighbours_to_vertex = True
            for element_name in clique:
                all_elements_in_clique_are_neighbours_to_vertex = all_elements_in_clique_are_neighbours_to_vertex and g.is_neighbour(vertex_name,element_name)
                if not all_elements_in_clique_are_neighbours_to_vertex:
                    break
#             print(vertex_name,all_elements_in_clique_are_neighbours_to_vertex )
            if all_elements_in_clique_are_neighbours_to_vertex:
                clique.add(vertex_name)
    return clique



def initial_heuristic_color_reverse():
    """
    makes clique:
    first - vericies with maximal color
    """

    clique = set()
    g.sort_vertex_by_degree()
    
    for color in range(len(g.used_colors)-1,-1,-1):
        for vertex_name in g.used_colors[color]:
            all_elements_in_clique_are_neighbours_to_vertex = True
            for element_name in clique:
                all_elements_in_clique_are_neighbours_to_vertex = all_elements_in_clique_are_neighbours_to_vertex and g.is_neighbour(vertex_name,element_name)
                if not all_elements_in_clique_are_neighbours_to_vertex:
                    break
#             print(vertex_name,all_elements_in_clique_are_neighbours_to_vertex )
            if all_elements_in_clique_are_neighbours_to_vertex:
                clique.add(vertex_name)
    return clique


def candidates_used_colors(candidates:set):
    """
    работает только для первоначальной покраски командами для класса Graph()
    для проверки количества цветов уже перекрашенного множества candidates (с помощью candidates_recolor) использовать 
    len(candidates_coloring)
    """
    used_colors = set()
    for vertex_name in candidates:
        used_colors.add(g.V[vertex_name]['color'])
    return used_colors



def candidates_recolor_new_dict(candidates:set):
    """
    Использовать с candidates при ветвлении
    т.к в первоначальной окраске слишком много цветов
    скорее всего стоит красить не каждое ветвление, а мб только в начале
    """
    max_color = -1
    candidates_coloring = dict()
    for vertex_name in candidates:
        candidates_coloring[vertex_name] = None
    used_colors = dict()
    for vertex_name in candidates:
        avalible_colors = set(used_colors.keys() )
        for neighbour_name in g.V[vertex_name]['neighbours'].intersection(candidates):
            avalible_colors -= {candidates_coloring[neighbour_name]}
            if len( avalible_colors ) == 0:
                break
        if len( avalible_colors ) == 0:
            max_color += 1 # color is index in candidates_coloring
            used_colors[max_color] = set()
            used_colors[max_color].add(vertex_name)
            candidates_coloring[vertex_name] = max_color
        if len( avalible_colors ) != 0:
            for avalible_color in avalible_colors:
                rand_avalible_color = avalible_color
                break
            used_colors[rand_avalible_color].add(vertex_name)
            candidates_coloring[vertex_name] = rand_avalible_color
    return used_colors,candidates_coloring



def candidates_recolor_degree(candidates:set, rev = True):
    """
    Использовать с candidates при ветвлении
    т.к в первоначальной окраске слишком много цветов
    скорее всего стоит красить не каждое ветвление, а мб только в начале
    """
    candidates_degree_order = list(candidates)
    candidates_degree_order.sort(key= lambda input: g.V[input]['degree'], reverse = rev)
    max_color = -1
    candidates_coloring = dict()
    for vertex_name in candidates:
        candidates_coloring[vertex_name] = None
    used_colors = dict()
    for vertex_name in candidates_degree_order:
        avalible_colors = set(used_colors.keys() )
        for neighbour_name in g.V[vertex_name]['neighbours'].intersection(candidates):
            avalible_colors -= {candidates_coloring[neighbour_name]}
            if len( avalible_colors ) == 0:
                break
        if len( avalible_colors ) == 0:
            max_color += 1 # color is index in candidates_coloring
            used_colors[max_color] = set()
            used_colors[max_color].add(vertex_name)
            candidates_coloring[vertex_name] = max_color
        if len( avalible_colors ) != 0:
            for avalible_color in avalible_colors:
                rand_avalible_color = avalible_color
                break
            used_colors[rand_avalible_color].add(vertex_name)
            candidates_coloring[vertex_name] = rand_avalible_color
    return used_colors,candidates_coloring



def find_candidates():
    """
    verticies - set of verticies names
    find all verticies, that are neigbours to all verticies in verticies
    if enter is empty - find all verticies of graph
    clique - глабавльная переменная
    """
    global clique
    candidates = set()
    if len(clique) == 0:
        candidates = set( g.V.keys() )
    for x in clique:
        candidates = g.V[x]['neighbours'].copy()
        break
    for vertex in clique:
        candidates.intersection_update(g.V[vertex]['neighbours'])
    return candidates


def branching_order():
    """
    создает последовательность из вершин множества candidates такую, что в начало добавляются
    те вершины, при добавлении которых в клику новое множество кандидаы расскрашивается 
    в большое количество цветов.
    Если понятно, что ветвь не оптимальна, то она сразу не добавляется в очередь
    """
    
    global clique, candidates, len_max_current_clique
    
    order = []
    colors_on_branch = []
    for vertex in candidates:
        clique.add(vertex)
        candidates_br = find_candidates()
        (colors_br,_) = candidates_recolor_degree(candidates_br)
        len_max_possible_clique_on_branch = len(colors_br) + len(clique)
        if len_max_possible_clique_on_branch  > len_max_current_clique: #debug +100
            order.append(vertex)
            colors_on_branch.append( len(colors_br) )
        clique.remove(vertex)
            
    x = zip(order,colors_on_branch)
    xs = sorted(x, key=lambda tup: tup[1], reverse = True)
    order = [x[0] for x in xs]
    colors_on_branch = [x[1] for x in xs] 

    return order,colors_on_branch


def branching_new():
    """
    прочитать граф
    расскрасить граф
    найти эвристику
    """
    global clique, candidates, len_max_current_clique, forbiden
    
    if len(candidates) == 0:
        len_max_current_clique = len(clique)
        
        print('Over of one branch. New max_clique = ', len_max_current_clique )
        print('clique is', clique)
        return
    
    order,colors_on_branch = branching_order()
    forbiden_br = dict()
    for vertex_index in range(len(order)):
        vertex = order[vertex_index]
        if colors_on_branch[vertex_index] + len(clique) + 1 <= len_max_current_clique: #debug +100
            continue
        clique.add(vertex)
        candidates = find_candidates()
        if not set(forbiden.keys()).issubset(candidates):
            clique.remove(vertex)
            if vertex in forbiden:
                forbiden[vertex] += 1
            else:
                forbiden[vertex] = 1

            if vertex in forbiden_br:
                forbiden_br[vertex] += 1
            else:
                forbiden_br[vertex] = 1
            continue
        (colors_br,_) = candidates_recolor_degree(candidates)
        len_max_possible_clique_on_branch = len(colors_br) + len(clique)
        #len_max_possible_clique_on_branch = 1000 # debug - del cell for work
        if len_max_possible_clique_on_branch > len_max_current_clique:
            branching_new()
        clique.remove(vertex)
        if vertex in forbiden:
            forbiden[vertex] += 1
        else:
            forbiden[vertex] = 1
        
        if vertex in forbiden_br:
            forbiden_br[vertex] += 1
        else:
            forbiden_br[vertex] = 1
        
    for vertex in forbiden_br:
        forbiden[vertex] -= forbiden_br[vertex]
        if forbiden[vertex] == 0:
            forbiden.pop(vertex)
        if vertex in forbiden and forbiden[vertex] < 0:
            raise AssertionError('forbiden[vertex] < 0')
    forbiden_br = dict()

path = 'C250.9.clq.txt'
path2 = 'C500.9.clq.txt'
path3 = 'brock800_4.clq.txt'
path4 = 'C125.9.clq.txt'
path_test = 'test.txt'

g = read_dimacs_graph(path4);

g.recolor()
c1 = len(g.used_colors)
g.clear_coloring()

g.recolor_by_degree()
c2 = len(g.used_colors)
g.clear_coloring()

g.recolor_by_degree_reverse()
c3 = len(g.used_colors)
g.clear_coloring()

if c1 is min(c1,c2,c3):
    g.clear_coloring()
    g.recolor()
    
if c2 is min(c1,c2,c3):
    g.recolor_by_degree()
    g.recolor()
if c3 is min(c1,c2,c3):
    g.recolor_by_degree_reverse()
    g.recolor()


init_clique = initial_heuristic_color()
init_clique_rev = initial_heuristic_color_reverse()
init_clique_degree = initial_heuristic_degree_2()



clique = set()
candidates = find_candidates()

len_max_current_clique = max( len(init_clique),len(init_clique_rev),len(init_clique_degree)  )
forbiden = dict()
branching_new()
