import networkx as nx
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import time

pathsToFiles = [
<<<<<<< Updated upstream:embedded/Old functions/teepwalk.py
    r"C:\Users\Admin\Desktop\Graph_Project\Files\aim-100-1_6-no-1.cnf",
    r"C:\Users\Admin\Desktop\Graph_Project\Files\aim-50-1_6-yes1-4.cnf",
    r"C:\Users\Admin\Desktop\Graph_Project\Files\bf0432-007.cnf"
]
=======
   
    #Easy
    r"Z:\Git\Graph_Project\Files\easy\sat\Analiza1-itox_vc1033.cnf",#0
    r"Z:\Git\Graph_Project\Files\easy\sat\Analiza2-rpoc_xits_15_SAT.cnf",#1
    r"Z:\Git\Graph_Project\Files\easy\unsat\Analiza1-post-cbmc-aes-ele-noholes.cnf",#2
    r"Z:\Git\Graph_Project\Files\easy\unsat\Analiza2-een-tip-uns-nusmv-t5.B.cnf",#3
>>>>>>> Stashed changes:Old functions/teepwalk.py

    #Medium
    r"Z:\Git\Graph_Project\Files\medium\sat\Analiza1-vmpc_29.cnf",#4
    r"Z:\Git\Graph_Project\Files\medium\sat\Analiza2-E02F20.cnf",#5
    r"Z:\Git\Graph_Project\Files\medium\sat\Analiza3-openstacks-p30_3.085-SAT.cnf",#6
    r"Z:\Git\Graph_Project\Files\medium\sat\Analiza4-ACG-15-10p1.cnf",#7
    r"Z:\Git\Graph_Project\Files\medium\unsat\Analiza1-AProVE07-08.cnf",#8
    r"Z:\Git\Graph_Project\Files\medium\unsat\Analiza2-manol-pipe-g10bid_i.cnf",#9
    r"Z:\Git\Graph_Project\Files\medium\unsat\Analiza3-grid-strips-grid-y-3.035-NOTKNOWN.cnf",#10
    r"Z:\Git\Graph_Project\Files\medium\unsat\Analiza4-aaai10-planning-ipc5-pathways-17-step20.cnf",#11
    #Hard
    r"Z:\Git\Graph_Project\Files\hard\sat\Analiza1-gss-20-s100.cnf",#12
    r"Z:\Git\Graph_Project\Files\hard\sat\Analiza2-slp-synthesis-aes-top29.cnf",#13
    r"Z:\Git\Graph_Project\Files\hard\sat\Analiza3-vmpc_33.cnf",#14
    r"Z:\Git\Graph_Project\Files\hard\sat\Analiza4-partial-10-17-s.cnf",#15
    r"Z:\Git\Graph_Project\Files\hard\unsat\Analiza1-rbcl_xits_08_UNSAT.cnf",#16
    r"Z:\Git\Graph_Project\Files\hard\unsat\Analiza2-6s10.cnf",#17
    r"Z:\Git\Graph_Project\Files\hard\unsat\Analiza3-smtlib-qfbv-aigs-ext_con_032_008_0256-tseitin.cnf",#18
    r"Z:\Git\Graph_Project\Files\hard\unsat\Analiza4-hitag2-10-60-0-0xe14721bd199894a-99.cnf",#19

    #Very Hard
    r"Z:\Git\Graph_Project\Files\very-hard\unsat\Analiza1-openstacks-sequencedstrips-nonadl-nonnegated-os-sequencedstrips-p30_3.025-NOTKNOWN.cnf",#20
    r"Z:\Git\Graph_Project\Files\very-hard\sat\Analiza1-gss-25-s100.cnf",#21

    #Old
    r"Z:\Git\Graph_Project\Files\bf0432-007.cnf",#22
    r"Z:\Git\Graph_Project\Files\aim-50-1_6-yes1-4.cnf",#23
    r"Z:\Git\Graph_Project\Files\aim-100-1_6-no-1.cnf"#24
]
chosenFile = 21

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

# Przykładowy graf (możesz dostosować go do własnych potrzeb)
#graph = nx.Graph()
#graph.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9)])






# Parametry DeepWalk
walk_length = 10  # Długość pojedynczej wędrówki
num_walks = 5  # Liczba wędrówek zaczynających się od każdego węzła
vector_size = 16  # Rozmiar wektora osadzenia
window_size = 3  # Rozmiar okna w modelu Word2Vec

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

def main():
    clauses = read_cnf_file(pathsToFiles[chosenFile])
    graph = create_graph_from_cnf(clauses)

    # Calculate the degree of each node (number of connections)
    node_degrees = dict(graph.degree())

    # Sort nodes by degree in descending order
    sorted_nodes = sorted(node_degrees, key=lambda x: node_degrees[x], reverse=True)

    # Normalize degrees to be between 0 and 1
    min_degree = min(node_degrees.values())
    max_degree = max(node_degrees.values())
    normalized_degrees = {node: 1 - ((node_degrees[node] - min_degree) / (max_degree - min_degree)) for node in graph.nodes()}

<<<<<<< Updated upstream:embedded/Old functions/teepwalk.py
plt.show()

for node in graph.nodes:
        node_representation = model.wv.get_vector(str(node))
        print(f"Node {node} representation:", node_representation)
elapsed_time = time.time() - start_time  # Calculate elapsed time
print(f"Graph creation and Node2Vec took {elapsed_time:.2f} seconds.")
=======
    # Create a color map based on normalized node degrees
    color_map = {node: plt.cm.RdYlGn(normalized_degrees[node]) for node in graph.nodes()}

    # Generowanie wędrówek
    walks = generate_walks(graph, num_walks, walk_length)

    # Utworzenie modelu Word2Vec na podstawie wędrówek
    model = Word2Vec(walks, vector_size=vector_size, window=window_size, sg=1, workers=4)

    # Rysowanie grafu
    pos = nx.spring_layout(graph)  # Układ wiosennego grafu
    nx.draw(graph, pos, with_labels=False, font_weight='bold', node_color=list(color_map.values()), node_size=700, font_size=8)

    # Dodanie legendy
    norm = plt.Normalize(0, 1)
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlGn, norm=norm)
    sm.set_array([])

    # Dodanie kolorowej mapy (colorbar) z dwiema wartościami
    cbar = plt.colorbar(sm, ticks=[0, 1], label='Normalized Node Degree', ax=plt.gca())

    # Zmiana etykiet na min i max
    cbar.set_ticklabels(['max', 'min'])
    
    plt.show()
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    print("Plik:", chosenFile)
    print(f"Graph creation and Node2Vec took {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    print("Metoda DeepWalk")
    #for chosenFile in range (22):
    #   for i in range(10):
    chosenFile = 23
    main()
>>>>>>> Stashed changes:Old functions/teepwalk.py
