import networkx as nx
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import time



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

# Funkcja generująca wędrówki w grafie
def generate_walks(graph, num_walks, walk_length):
        walks = []
        for _ in range(num_walks):
            for node in graph.nodes():
                walk = [node]
                for _ in range(walk_length - 1):
                    neighbors = list(graph.neighbors(walk[-1]))
                    if neighbors:
                        walk.append(neighbors[0])  # Wybieramy losowego sąsiada
                    else:
                        break
                walks.append([str(node) for node in walk])
        return walks

def deepWalk(filePath):

    clauses = read_cnf_file(filePath)
    graph = create_graph_from_cnf(clauses)

    start_time = time.time()  # Record the start time


    # Parametry DeepWalk
    walk_length = 10  # Długość pojedynczej wędrówki
    num_walks = 5  # Liczba wędrówek zaczynających się od każdego węzła
    vector_size = 16  # Rozmiar wektora osadzenia
    window_size = 3  # Rozmiar okna w modelu Word2Vec

    
    

    # Generowanie wędrówek
    walks = generate_walks(graph, num_walks, walk_length)

    # Utworzenie modelu Word2Vec na podstawie wędrówek
    model = Word2Vec(walks, vector_size=vector_size, window=window_size, sg=1, workers=4)

    # Rysowanie grafu
    pos = nx.spring_layout(graph)  # Układ wiosennego grafu
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=700, font_size=8)

    # Dodanie etykiet do węzłów z osadzeniami
    for node, (x, y) in pos.items():
        plt.text(x, y, f"{node}\n{model.wv[str(node)]}", fontsize=6, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    #plt.show()
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    #print(f"Graph creation and Node2Vec took {elapsed_time:.2f} seconds.")

    return graph,model,elapsed_time