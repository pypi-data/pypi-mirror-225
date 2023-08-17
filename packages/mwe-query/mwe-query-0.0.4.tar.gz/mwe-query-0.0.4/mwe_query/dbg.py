import graphviz


def node_fmt(node):
    word, idx, cat, rel, pt = node.attrib.get('word', ''), node.attrib.get('index', ''), node.attrib.get('cat', ''), node.attrib.get('rel', ''), node.attrib.get('pt', '')
    return f'{word} (index={idx};cat={cat};rel={rel};pt={pt})'

def node_edges(node):
    edges = []
    # visited = set()
    for child in node.findall('./node'):
        # if child in visited:
            # return edges
        # visited.add(child)
        if node != child:
            edges.append((node, child))

    return edges

def graph_tree(tree, name):
    graph = graphviz.Digraph('bla')
    visited = set()
    for node in tree.iter():
        if node in visited:
            break
        visited.add(node)
        graph.node(hex(id(node)), node_fmt(node))

    for node in visited:
        for edge in node_edges(node):
            graph.edge(hex(id(edge[0])), hex(id(edge[1])))

    # now paint route
    from collections import defaultdict
    visited = defaultdict(int)
    prev = tree.getroot()
    for node in tree.iter():
        # graph.add_edge(node_fmt(prev), node_fmt(node), color='blue')
        if visited[node] > 0:
            graph.edge(hex(id(prev)), hex(id(node)), color='red')
        if visited[node] > 1:
            break
        prev = node
        visited[node] += 1
        print(node.attrib.get('word', ''), end=' ')


    print('\n' + '-' * 15)
    graph.render(filename='/tmp/' + name, view=True, format='png', engine='dot')

# import pygraphviz


# def node_fmt(node):
#     word, cat, rel = node.attrib.get('word', ''), node.attrib.get('cat', ''), node.attrib.get('rel', '')
#     return hex(id(node)) + f': {word}, {cat}, {rel}'

# def node_edges(node):
#     edges = []
#     # visited = set()
#     for child in node.findall('./node'):
#         # if child in visited:
#             # return edges
#         # visited.add(child)
#         if node != child:
#             edges.append((node, child))

#     return edges

# def graph_tree(tree):
#     graph = pygraphviz.AGraph(directed=True)
#     visited = set()
#     for node in tree.iter():
#         if node in visited:
#             break
#         visited.add(node)
#         graph.add_node(node_fmt(node))

#     for node in visited:
#         for edge in node_edges(node):
#             graph.add_edge(node_fmt(edge[0]), node_fmt(edge[1]))

#     # now paint route
#     from collections import defaultdict
#     visited = defaultdict(int)
#     prev = tree.getroot()
#     for node in tree.iter():
#         # graph.add_edge(node_fmt(prev), node_fmt(node), color='blue')
#         if visited[node] > 0:
#             graph.add_edge(node_fmt(prev), node_fmt(node), color='red')
#         if visited[node] > 1:
#             break
#         prev = node
#         visited[node] += 1


#     graph.draw('/tmp/dbg.png', prog='dot')
