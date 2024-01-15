import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import time
import os
import sys

# Ścieżka bieżąca (aktualny katalog)
aktualna_sciezka = sys.argv[0]
aktualna_sciezka = os.path.dirname(os.path.dirname(aktualna_sciezka))
pathsToFiles = [
    
    #Easy
    r"Files\easy\sat\Analiza1-itox_vc1033.cnf",#0
    r"Files\easy\sat\Analiza2-rpoc_xits_15_SAT.cnf",#1
    r"Files\easy\unsat\Analiza1-post-cbmc-aes-ele-noholes.cnf",#2
    r"Files\easy\unsat\Analiza2-een-tip-uns-nusmv-t5.B.cnf",#3

    #Medium
    r"Files\medium\sat\Analiza1-vmpc_29.cnf",#4
    r"Files\medium\sat\Analiza2-E02F20.cnf",#5
    r"Files\medium\sat\Analiza3-openstacks-p30_3.085-SAT.cnf",#6
    r"Files\medium\sat\Analiza4-ACG-15-10p1.cnf",#7
    r"Files\medium\unsat\Analiza1-AProVE07-08.cnf",#8
    r"Files\medium\unsat\Analiza2-manol-pipe-g10bid_i.cnf",#9
    r"Files\medium\unsat\Analiza3-grid-strips-grid-y-3.035-NOTKNOWN.cnf",#10
    r"Files\medium\unsat\Analiza4-aaai10-planning-ipc5-pathways-17-step20.cnf",#11

    #Hard
    r"Files\hard\sat\Analiza1-gss-20-s100.cnf",#12
    r"Files\hard\sat\Analiza2-slp-synthesis-aes-top29.cnf",#13
    r"Files\hard\sat\Analiza3-vmpc_33.cnf",#14
    r"Files\hard\sat\Analiza4-partial-10-17-s.cnf",#15
    r"Files\hard\unsat\Analiza1-rbcl_xits_08_UNSAT.cnf",#16
    r"Files\hard\unsat\Analiza2-6s10.cnf",#17
    r"Files\hard\unsat\Analiza3-smtlib-qfbv-aigs-ext_con_032_008_0256-tseitin.cnf",#18
    r"Files\hard\unsat\Analiza4-hitag2-10-60-0-0xe14721bd199894a-99.cnf",#19

    #Very Hard
    r"Files\very-hard\unsat\Analiza1-openstacks-sequencedstrips-nonadl-nonnegated-os-sequencedstrips-p30_3.025-NOTKNOWN.cnf",#20
    r"Files\very-hard\sat\Analiza1-gss-25-s100.cnf",#21

    #Old
    r"Files\bf0432-007.cnf",#22
    r"Files\aim-50-1_6-yes1-4.cnf",#23
    r"Files\aim-100-1_6-no-1.cnf"#24
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

# Parametry DeepWalk
walk_length = 10  # Długość pojedynczej wędrówki
num_walks = 5  # Liczba wędrówek zaczynających się od każdego węzła
vector_size = 16  # Rozmiar wektora osadzenia
window_size = 3  # Rozmiar okna w modelu Word2Vec

def generate_walks(graph, num_walks, walk_length):
    walks = []
    for _ in range(num_walks):
        for node in graph.nodes():
            walk = [node]
            for _ in range(walk_length - 1):
                neighbors = list(graph.neighbors(walk[-1]))
                if neighbors:
                    walk.append(neighbors[0])  # Wybieramy losowego sÄsiada
                else:
                    break
            walks.append([str(node) for node in walk])
    return walks

def visualize_deepwalk_results(graph, embedding):
    tsne = TSNE(n_components=2, random_state=42)
    embedding_tsne = tsne.fit_transform(embedding)

    # Get the nodes with deep walk embeddings
    deepwalk_nodes = set(graph.nodes())

    # Rysowanie grafu bez niebieskich węzłów
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(graph)
    
    # Rysowanie węzłów bez etykiet
    nx.draw_networkx_nodes(graph, pos=pos, nodelist=[node for node in graph.nodes() if node not in deepwalk_nodes], node_size=700, node_color='lightgray')

    # Dodanie etykiet do węzłów
    labels = {}
    for node in graph.nodes():
        if node in deepwalk_nodes:
            labels[node] = str(node)

    # Dodanie punktów reprezentujących węzły z DeepWalk
    scatter = plt.scatter(embedding_tsne[:, 0], embedding_tsne[:, 1], marker='o', s=100, color='red', edgecolors='darkred', linewidths=1.5, label='t-SNE')

    # Dodanie legendy
    plt.legend()

    # Dodanie etykiet do każdego punktu w środku z obramowaniem
    for i, label in enumerate(labels):
        x, y = embedding_tsne[i, 0], embedding_tsne[i, 1]
        plt.text(x, y, label, ha='center', va='center', fontsize=8, bbox=dict(facecolor='red', edgecolor='darkred', boxstyle='circle,pad=0.3'))

    plt.show()


def main():
    clauses = read_cnf_file(aktualna_sciezka)
    graph = create_graph_from_cnf(clauses)

    # Calculate the degree of each node (number of connections)
    node_degrees = dict(graph.degree())

    # Sort nodes by degree in descending order
    sorted_nodes = sorted(node_degrees, key=lambda x: node_degrees[x], reverse=True)

    # Normalize degrees to be between 0 and 1
    min_degree = min(node_degrees.values())
    max_degree = max(node_degrees.values())
    normalized_degrees = {node: 1 - ((node_degrees[node] - min_degree) / (max_degree - min_degree)) for node in graph.nodes()}

   
    # Generowanie wędrówek
    walks = generate_walks(graph, num_walks, walk_length)

    # Utworzenie modelu Word2Vec na podstawie wÄdrÃ³wek
    model = Word2Vec(walks, vector_size=vector_size, window=window_size, sg=1, workers=4)

    # Pobranie wynikÃ³w DeepWalk (embedding)
    embedding = np.array([model.wv[str(node)] for node in graph.nodes()])

    # Wizualizacja wynikÃ³w DeepWalk przy uÅ¼yciu t-SNE
    visualize_deepwalk_results(graph, embedding)
    # Rysowanie grafu
    

    

    

   
    
    plt.show()

    for node in graph.nodes:
        node_representation = model.wv.get_vector(str(node))
        print(f"Node {node} representation:", node_representation)
    
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    print(f"Graph creation and Node2Vec took {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    
    start_time = time.time()  # Start measuring time
    print("SSSSSSSSSSSSSS")
    #for chosenFile in range (22):
    #   for i in range(10):
    chosenFile = 1

    aktualna_sciezka = aktualna_sciezka + '\\' + pathsToFiles[chosenFile]
    #print(aktualna_sciezka)
    main()