import networkx as nx
from node2vec import Node2Vec
import matplotlib.pyplot as plt
import time

pathsToFiles = [
    r"C:\Users\Admin\Desktop\Graph_Project\Files\aim-100-1_6-no-1.cnf",
    r"C:\Users\Admin\Desktop\Graph_Project\Files\aim-50-1_6-yes1-4.cnf",
    r"C:\Users\Admin\Desktop\Graph_Project\Files\bf0432-007.cnf"
]

chosenFile = 0

def read_cnf_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    clauses = []
    for line in lines:
        if line.startswith('c') or line.startswith('p'):
            continue
        clause = list(map(int, line.split()[:-1]))
        clauses.append(clause)

    return clauses

def create_graph_from_cnf(clauses):
    G = nx.Graph()

    for clause in clauses:
        for literal in clause:
            G.add_node(abs(literal))

    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                G.add_edge(abs(clause[i]), abs(clause[j]))

    return G

def plot_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold')
    plt.show()

def main():
    start_time = time.time()  # Record the start time

    clauses = read_cnf_file(pathsToFiles[chosenFile])
    graph = create_graph_from_cnf(clauses)
    #plot_graph(graph)
    

    node2vec = Node2Vec(graph, dimensions=64, walk_length=30, num_walks=200, workers=4)
    model = node2vec.fit(window=10, min_count=1, batch_words=4)

    #elapsed_time = time.time() - start_time  # Calculate elapsed time

    

    
    for node in graph.nodes:
        node_representation = model.wv.get_vector(str(node))
        print(f"Node {node} representation:", node_representation)

    #node_representation = model.wv.get_vector('1')

    #print(f"Graph creation and Node2Vec took {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
