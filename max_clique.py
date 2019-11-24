from graph import Graph, read_dimacs_graph


def candidates_recolor(candidates: set):
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
            if len(neighbour_colors) == len(used_colors):
                #                 print('break')
                break
        if len(neighbour_colors) == len(used_colors):
            max_color += 1  # color is index in candidates_coloring
            used_colors[max_color] = set()
            used_colors[max_color].add(vertex_name)
            candidates_coloring[vertex_name] = max_color
        #             print(used_colors,candidates_coloring)

        #         print('available_colors',available_colors)
        elif len(neighbour_colors) < len(used_colors):
            available_colors = set(used_colors.keys()) - neighbour_colors
            #             print('available_colors',available_colors)
            for available_color in available_colors:
                rand_available_color = available_color
                break
            used_colors[rand_available_color].add(vertex_name)
            candidates_coloring[vertex_name] = rand_available_color
    #         print('chosen_Color',candidates_coloring[vertex_name])
    if len(candidates_coloring) != len(candidates):
        raise NameError('Not all vertices colored')
    return used_colors, candidates_coloring


def candidates_recolor_degree(candidates: set, rev=True):
    """
    Использовать с candidates при ветвлении
    т.к в первоначальной окраске слишком много цветов
    скорее всего стоит красить не каждое ветвление, а мб только в начале
    """
    candidates_degree_order = list(candidates)
    candidates_degree_order.sort(key=lambda input: g.V[input]['degree'], reverse=rev)
    max_color = -1
    candidates_coloring = dict()
    for vertex_name in candidates:
        candidates_coloring[vertex_name] = None
    used_colors = dict()
    for vertex_name in candidates_degree_order:
        available_colors = set(used_colors.keys())
        for neighbour_name in g.V[vertex_name]['neighbours'].intersection(candidates):
            available_colors -= {candidates_coloring[neighbour_name]}
            if len(available_colors) == 0:
                break
        if len(available_colors) == 0:
            max_color += 1  # color is index in candidates_coloring
            used_colors[max_color] = set()
            used_colors[max_color].add(vertex_name)
            candidates_coloring[vertex_name] = max_color
        if len(available_colors) != 0:
            for available_color in available_colors:
                rand_available_color = available_color
                break
            used_colors[rand_available_color].add(vertex_name)
            candidates_coloring[vertex_name] = rand_available_color
    return used_colors, candidates_coloring


def find_candidates(vertex_to_clique=None):
    """
    если клика пустая создает множество из всех вершин графа
    если не пустая выдает ошибку - использовать update_candidates
    """
    global clique, candidates

    if len(clique) == 0:
        candidates = set(g.V.keys())
    else:
        raise NameError('len(clique) =! 0. Use update_candidates')

    return candidates


def update_candidates(used_candidates=None, candidates=None, vertex_to_clique=None):
    """
    если клика пустая выдает ошибку - нужно использовать find_candidates
    если клика не пустая то обновляет множетсво кандидитов:
        в него включаются те вершины, которые есть в кандидатах
        и те вершины, которые есть в соседях у вершины vertex_to_clique, которая
        в данный момент добавляется в клику
    """
    global clique  # , candidates

    if len(clique) == 0:
        raise NameError('len(clique) == 0. Use find_candidates')
    if candidates is None:
        raise NameError('candidates = None')
    if used_candidates is None:
        used_candidates = set()
    else:
        if vertex_to_clique not in candidates:
            raise NameError(vertex_to_clique, 'No such vertex in candidates')
        updated_candidates = candidates.intersection(g.V[vertex_to_clique]['neighbours']) - used_candidates
    return updated_candidates


def branching_order(candidates, colors):
    """
    создает последовательность из вершин множества candidates такую, что в начало добавляются
    те вершины, при добавлении которых в клику новое множество кандидаы расскрашивается 
    в большое количество цветов.
    Если понятно, что ветвь не оптимальна, то она сразу не добавляется в очередь
    """

    global clique, len_max_current_clique  # , colors # candidates,
    colors_num = len(colors)  # colors надо полуить до использования функции
    candidates_order = []
    # len(clique) + color of vertex > len_max_current_clique
    # дальше используем вершины с цветом, удовлетворяющим этому условию
    # colors = 0,1,2,3,4...
    last_color = len_max_current_clique - len(clique)  # вроде без +1
    for color in range(colors_num - 1, max(last_color - 1, -1), -1):
        for vertex in colors[color]:
            if vertex not in clique:
                candidates_order.append(vertex)

    return candidates_order


def branching_new(candidates, used_candidates):
    """
    прочитать граф
    расскрасить граф
    найти эвристику
    """
    global clique, len_max_current_clique, min_in, max_out  # , candidates

    if len(candidates) == 0:
        len_max_current_clique = len(clique)
        print('Over of one branch. New max_clique = ', len_max_current_clique)
        print('clique is', clique)
        return

    (colors, vertex_coloring) = candidates_recolor(candidates)
    colors_num_of_candidates = len(colors)
    if colors_num_of_candidates + len(clique) < len_max_current_clique:
        return
    candidates_order = branching_order(candidates, colors)
    if min_in > len(candidates_order):
        min_in = len(candidates_order)
        print(min_in)
    for vertex in candidates_order:
        vertex_color = vertex_coloring[vertex]
        if (vertex_color + 1) + len(
                clique) <= len_max_current_clique:  # len_max_current_clique может измениться. Поэтому проверяем
            for vertex_1 in candidates_order:
                if vertex_1 == vertex:
                    break
                used_candidates.remove(vertex_1)
            break  # все вершиниы дальше по списку тоже не удовлетворяют этому условию
        clique.add(vertex)
        candidates_br = update_candidates(used_candidates, candidates, vertex_to_clique=vertex)
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

if c1 is min(c1, c2, c3):
    g.clear_coloring()
    g.recolor()

if c2 is min(c1, c2, c3):
    g.recolor_by_degree()
    g.recolor()
if c3 is min(c1, c2, c3):
    g.recolor_by_degree_reverse()
    g.recolor()

clique = set()
candidates = find_candidates()
min_in = 125
max_out = 0
len_max_current_clique = g.find_init_heuristic()
used_candidates = set()
branching_new(candidates, used_candidates)
