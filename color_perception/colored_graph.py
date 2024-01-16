import networkx as nx
import matplotlib.pyplot as plt
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

    # Create a color map based on normalized node degrees
    color_map = {node: plt.cm.RdYlGn(normalized_degrees[node]) for node in graph.nodes()}

    # Rysowanie grafu
    pos = nx.spring_layout(graph)  # Układ wiosennego grafu
    nx.draw(graph, pos, with_labels=False, font_weight='bold', node_color=list(color_map.values()), node_size=700, font_size=8)

    # Dodanie numerów wierzchołków
    node_labels = {node: str(node) for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=8, font_color='black')

   # Wypisz numery 3 wierzchołków o największej liczbie połączeń
    print("Top 3 wierzchołki o największej liczbie połączeń:")
    for node in sorted_nodes[:3]:
        print(f"{node} - {node_degrees[node]}")

    # Wypisz numery 3 wierzchołków o najmniejszej liczbie połączeń
    print("\nTop 3 wierzchołki o najmniejszej liczbie połączeń:")
    for node in sorted_nodes[-3:]:
        print(f"{node} - {node_degrees[node]}")

    

    # Dodanie legendy
    norm = plt.Normalize(0, 1)
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlGn, norm=norm)
    sm.set_array([])

    # Dodanie kolorowej mapy (colorbar) z dwiema wartościami
    cbar = plt.colorbar(sm, ticks=[0, 1], label='Normalized Node Degree', ax=plt.gca(), orientation='horizontal', pad=0.1)  # Ustawienie pad na 0.1, aby dostosować długość

    # Zmiana etykiet na max i min
    cbar.set_ticklabels([max_degree, min_degree])

    # Wyśrodkowanie legendy
    cbar.ax.set_position([0.05, 0.01, 0.89, 0.1])  # Ustawienie pozycji

    plt.show()

    
if __name__ == "__main__":
    
    #for chosenFile in range (22):
    #   for i in range(10):
    chosenFile = 1
    aktualna_sciezka = aktualna_sciezka + '\\' + pathsToFiles[chosenFile]
    #print(aktualna_sciezka)
    main()