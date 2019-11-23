

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
            self.D.append(self.V[v1])
            self._D_sorted = False
            
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
        
            
    
    def clear_coloring(self):
        self.used_colors = set()
        self.coloring = dict()

        
    def recolor(self):
        """
        Использовать с candidates при ветвлении
        т.к в первоначальной окраске слишком много цветов
        скорее всего стоит красить не каждое ветвление, а мб только в начале
        """
    #     print('***recolor***')
        max_color = -1
        self.coloring = dict()
        for vertex_name in self.V:
            self.coloring[vertex_name] = None
        self.used_colors = dict()
        for vertex_name in self.V:
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
#         return used_colors,candidates_coloring

    def recolor_by_degree(self):
        """
        Использовать с candidates при ветвлении
        т.к в первоначальной окраске слишком много цветов
        скорее всего стоит красить не каждое ветвление, а мб только в начале
        """
    #     print('***recolor***')    
        self.sort_vertex_by_degree()
        max_color = -1
        self.coloring = dict()
        for vertex_name in self.V:
            self.coloring[vertex_name] = None
        self.used_colors = dict()
        for vertex in self.D:
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

    def recolor_by_degree_reverse(self):
            """
            Использовать с candidates при ветвлении
            т.к в первоначальной окраске слишком много цветов
            скорее всего стоит красить не каждое ветвление, а мб только в начале
            """
        #     print('***recolor***')    
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
    #   
    
        

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
                g.add_edge(int(v1),int(v2))
            else:
                continue
        return g


def initial_heuristic_degree():
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





def candidates_recolor(candidates:set):
    """
    Использовать с candidates при ветвлении
    т.к в первоначальной окраске слишком много цветов
    скорее всего стоит красить не каждое ветвление, а мб только в начале
    """
#     print('***candidates_recolor***')
    max_color = 0
    candidates_coloring = dict()
    for vertex_name in candidates:
        candidates_coloring[vertex_name] = 0
    used_colors = {0: set()}
    for vertex_name in candidates:
#         print('vertex_name',vertex_name)
#         print('used_Colors',used_colors)
        neighbour_colors = set()
        for neighbour_name in g.V[vertex_name]['neighbours'].intersection(candidates):
#             print('N',neighbour_name, candidates_coloring[neighbour_name] , neighbour_name in candidates)
            neighbour_colors.add(candidates_coloring[neighbour_name])
            if len( neighbour_colors ) == len(used_colors):
#                 print('break')
                break
        if len( neighbour_colors ) == len(used_colors):
            max_color += 1 # color is index in candidates_coloring
            used_colors[max_color] = set()
            used_colors[max_color].add(vertex_name)
            candidates_coloring[vertex_name] = max_color
#             print(used_colors,candidates_coloring)
        
#         print('avalible_colors',avalible_colors)
        elif len( neighbour_colors ) < len(used_colors):
            avalible_colors = set(used_colors.keys()) - neighbour_colors
#             print('avalible_colors',avalible_colors)
            for avalible_color in avalible_colors:
                rand_avalible_color = avalible_color
                break
            used_colors[rand_avalible_color].add(vertex_name)
            candidates_coloring[vertex_name] = rand_avalible_color
#         print('chosen_Color',candidates_coloring[vertex_name])
    if len(candidates_coloring) != len(candidates):
        raise NameError('Not all verticies colored')
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



def find_candidates(vertex_to_clique = None):
    """
    если клика пустая создает множество из всех вершин графа
    если не пустая выдает ошибку - использовать update_candidates
    """
    global clique, candidates
    
    if len(clique) == 0:
        candidates = set( g.V.keys() )
    else:
        raise NameError('len(clique) =! 0. Use update_candidates')

    return candidates


def update_candidates(used_candidates = None, candidates = None, vertex_to_clique = None):
    """
    если клика пустая выдает ошибку - нужно использовать find_candidates
    если клика не пустая то обновляет множетсво кандидитов:
        в него включаются те вершины, которые есть в кандидатах
        и те вершины, которые есть в соседях у вершины vertex_to_clique, которая
        в данный момент добавляется в клику
    """
    global clique #, candidates
    
    if len(clique) == 0:
        raise NameError('len(clique) == 0. Use find_candidates')
    if candidates is None:
        raise NameError('candidates = None')
    if used_candidates is None:
        used_candidates = set()
    else:
        if vertex_to_clique not in candidates:
            raise NameError(vertex_to_clique,'No such vertex in candidates')
        updated_candidates = candidates.intersection(g.V[vertex_to_clique]['neighbours']) - used_candidates
    return updated_candidates


def branching_order(candidates,colors):
    """
    создает последовательность из вершин множества candidates такую, что в начало добавляются
    те вершины, при добавлении которых в клику новое множество кандидаы расскрашивается 
    в большое количество цветов.
    Если понятно, что ветвь не оптимальна, то она сразу не добавляется в очередь
    """
    
    global clique, len_max_current_clique #, colors # candidates,
    colors_num = len(colors) # colors надо полуить до использования функции
    candidates_order = []
    # len(cloque) + color of vertex > len_max_current_clique
    # дальше используем вершины с цветом, удовлетворяющим этому условию
    # colors = 0,1,2,3,4...
    last_color = len_max_current_clique - len(clique) # вроде без +1
    for color in range(colors_num - 1, max(last_color - 1,-1), -1):
        for vertex in colors[color]:
            if not vertex in clique:
                candidates_order.append(vertex)
    
    
    
    return candidates_order

def branching_new(candidates, used_candidates):
    """
    прочитать граф
    расскрасить граф
    найти эвристику
    """
    global clique, len_max_current_clique, min_in, max_out #, candidates
    
    if len(candidates) == 0:
        len_max_current_clique = len(clique)
        print('Over of one branch. New max_clique = ', len_max_current_clique )
        print('clique is', clique)
        return
    
    (colors,vertex_coloring) = candidates_recolor(candidates)
    colors_num_of_candidates = len(colors)
    if colors_num_of_candidates + len(clique) < len_max_current_clique:
        return
    candidates_order = branching_order(candidates,colors)
    if min_in > len(candidates_order):
        min_in = len(candidates_order)
        print(min_in)
    for vertex in candidates_order:
        vertex_color = vertex_coloring[vertex]
        if (vertex_color + 1) + len(clique) <= len_max_current_clique: # len_max_current_clique может измениться. Поэтому проверяем
            for vertex_1 in candidates_order:
                if vertex_1 == vertex:
                    break
                used_candidates.remove(vertex_1)
            break # все вершиниы дальше по списку тоже не удовлетворяют этому условию
        clique.add(vertex)
        candidates_br = update_candidates(used_candidates, candidates, vertex_to_clique = vertex)
        branching_new(candidates_br, used_candidates)
        used_candidates.add(vertex)
        clique.remove(vertex)
    else:
        for vertex in candidates_order:
            used_candidates.remove(vertex)
    if max_out < len(candidates_order):
        max_out = len(candidates_order)
        print(max_out)

path = 'C250.9.clq.txt'
path2 = 'C500.9.clq.txt'
path3 = 'brock800_4.clq.txt'
path4 = 'C125.9.clq.txt'
path_test = 'test.txt'
path_test_2 = 'test2.txt'

g = read_dimacs_graph(path2);

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
init_clique_degree = initial_heuristic_degree()



clique = set()
candidates = find_candidates()
min_in = 125
max_out = 0
len_max_current_clique = max( len(init_clique),len(init_clique_rev),len(init_clique_degree)  )
used_candidates = set()
len_max_current_clique = 1
branching_new(candidates,used_candidates)