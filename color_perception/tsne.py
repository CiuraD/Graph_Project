import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import time
import os
import sys



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




def tsne(filePath):
    clauses = read_cnf_file(filePath)
    graph = create_graph_from_cnf(clauses)

    start_time = time.time()  # Record the start time

    # Parametry DeepWalk
    walk_length = 10  # Długość pojedynczej wędrówki
    num_walks = 5  # Liczba wędrówek zaczynających się od każdego węzła
    vector_size = 16  # Rozmiar wektora osadzenia
    window_size = 3  # Rozmiar okna w modelu Word2Vec



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

    elapsed_time = time.time() - start_time  # Calculate elapsed time
    #print(f"Graph creation and Node2Vec took {elapsed_time:.2f} seconds.")

    results = ""
    a = 0

    for node in graph.nodes:
        node_representation = model.wv.get_vector(str(node))
        results += f"Node {node} representation: {str(node_representation)}\n"
        a+=1
    

    return graph,results,elapsed_time,a