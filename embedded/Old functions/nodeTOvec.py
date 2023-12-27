import networkx as nx
from node2vec import Node2Vec
import matplotlib.pyplot as plt
import time

pathsToFiles = [
<<<<<<< Updated upstream:embedded/Old functions/nodeTOvec.py
    r"C:\Users\Admin\Desktop\Graph_Project\Files\aim-100-1_6-no-1.cnf",
    r"C:\Users\Admin\Desktop\Graph_Project\Files\aim-50-1_6-yes1-4.cnf",
    r"C:\Users\Admin\Desktop\Graph_Project\Files\bf0432-007.cnf"
=======
   
    #Easy
    #r"Z:\Git\Graph_Project\Files\easy\sat\Analiza1-itox_vc1033.cnf",#0 ####NIE DZIAŁA
    r"Z:\Git\Graph_Project\Files\easy\sat\Analiza2-rpoc_xits_15_SAT.cnf",#1
    r"Z:\Git\Graph_Project\Files\easy\unsat\Analiza1-post-cbmc-aes-ele-noholes.cnf",#2
    r"Z:\Git\Graph_Project\Files\easy\unsat\Analiza2-een-tip-uns-nusmv-t5.B.cnf",#3

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
    #OldFiles
    #r"Z:\Git\Graph_Project\Files\aim-50-1_6-yes1-4.cnf"#22
>>>>>>> Stashed changes:Old functions/nodeTOvec.py
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

    elapsed_time = time.time() - start_time  # Calculate elapsed time

    print("Plik:",chosenFile)
    #print("Podejście:",i)
    print(f"Graph creation and Node2Vec took {elapsed_time:.2f} seconds.")

    
    #for node in graph.nodes:
    #    node_representation = model.wv.get_vector(str(node))
    #    print(f"Node {node} representation:", node_representation)

    #node_representation = model.wv.get_vector('1')

    

if __name__ == "__main__":
    for chosenFile in range (20):
       #for i in range(10):
        main()