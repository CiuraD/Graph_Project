import nltk
nltk.download('punkt')
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import networkx as nx
import matplotlib.pyplot as plt
import time

pathsToFiles = [
<<<<<<< Updated upstream:embedded/Old functions/wordTOvec.py
    r"C:\Users\Admin\Desktop\Graph_Project\Files\aim-100-1_6-no-1.cnf",
    r"C:\Users\Admin\Desktop\Graph_Project\Files\aim-50-1_6-yes1-4.cnf",
    r"C:\Users\Admin\Desktop\Graph_Project\Files\bf0432-007.cnf"
=======
   
    #Easy
    r"Z:\Git\Graph_Project\Files\easy\sat\Analiza1-itox_vc1033.cnf",#0
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
    r"Z:\Git\Graph_Project\Files\very-hard\sat\Analiza1-gss-25-s100.cnf"#21
>>>>>>> Stashed changes:Old functions/wordTOvec.py
]

chosenFile = 21

# Załaduj dane CNF z pliku, ignorując linie zaczynające się od 'c' lub 'p cnf'
def load_cnf(file_path):
    cnf_data = ""
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith(('c', 'p cnf')):
                cnf_data += line
    return cnf_data

# Tokenizacja tekstu (możesz dostosować tę funkcję w zależności od struktury CNF)
def tokenize_cnf(cnf_data):
    return word_tokenize(cnf_data)

# Przygotuj dane do modelu Doc2Vec
def prepare_data(cnf_data):
    tokens = tokenize_cnf(cnf_data)
    tagged_data = [TaggedDocument(words=tokens, tags=['CNF'])]
    return tagged_data

# Rysuj graf CNF
def draw_cnf_graph(cnf_data):
    tokens = tokenize_cnf(cnf_data)
    G = nx.Graph()

    # Dodaj wierzchołki do grafu
    for token in tokens:
        G.add_node(token)

    # Dodaj krawędzie do grafu (możesz dostosować tę część w zależności od struktury CNF)
    for i in range(len(tokens)-1):
        G.add_edge(tokens[i], tokens[i+1])

    # Rysuj graf
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()

# Trenuj model Doc2Vec
def train_doc2vec_model(tagged_data):
    model = Doc2Vec(vector_size=100, window=2, min_count=1, workers=4, epochs=100)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    return model

def main():
    # Przykładowe użycie z dodanym stoperem
    start_time = time.time()

    cnf_data = load_cnf(pathsToFiles[chosenFile])
    tagged_data = prepare_data(cnf_data)
    model = train_doc2vec_model(tagged_data)

    # Uzyskaj osadzenia dla grafu CNF
    graph_embedding = model.dv['CNF']
    #print("Embedding for CNF:", graph_embedding)

    # Rysuj graf CNF
    #draw_cnf_graph(cnf_data)

    end_time = time.time()
    execution_time = end_time - start_time
    print("Plik:",chosenFile)
    print("Podejście:",i)
    print("Execution time: {:.2f} seconds".format(execution_time))

if __name__ == "__main__":
    for chosenFile in range (22):
       for i in range(10):
            main()
