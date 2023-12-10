import nltk
nltk.download('punkt')
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import networkx as nx
import matplotlib.pyplot as plt
import time

pathsToFiles = [
    r"C:\Users\Admin\Desktop\aim-100-1_6-no-1.cnf",
    r"C:\Users\Admin\Desktop\aim-50-1_6-yes1-4.cnf",
    r"C:\Users\Admin\Desktop\bf0432-007.cnf"
]

chosenFile = 2

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
    #plt.show()

    return G
    

# Trenuj model Doc2Vec
def train_doc2vec_model(tagged_data):
    model = Doc2Vec(vector_size=100, window=2, min_count=1, workers=4, epochs=100)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    return model

def doc2Vec(filePath):
    # Przykładowe użycie z dodanym stoperem
    start_time = time.time()

    cnf_data = load_cnf(filePath)
    tagged_data = prepare_data(cnf_data)
    model = train_doc2vec_model(tagged_data)

    # Uzyskaj osadzenia dla grafu CNF
    graph_embedding = model.dv['CNF']
    print("Embedding for CNF:", graph_embedding)

    # Rysuj graf CNF
    G = draw_cnf_graph(cnf_data)

    end_time = time.time()
    elapsed_time = end_time - start_time
    #print("Execution time: {:.2f} seconds".format(execution_time))

    return G,model,elapsed_time