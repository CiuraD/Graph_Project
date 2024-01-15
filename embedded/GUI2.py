import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from Methods.tsne import tsne
import webbrowser 
import os

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def run_tsne(graph):
    # Przekształć strukturę grafu na macierz sąsiedztwa
    adjacency_matrix = nx.to_numpy_array(graph)

    tsne = TSNE(n_components=2)
    embedding = tsne.fit_transform(adjacency_matrix)
    return embedding


def process_data(input_file, output_file):
    # Wczytaj plik CNF
    cnf_formula_str = ''.join(read_file(input_file))

    G, model, time, a = tsne(input_file)
    
    # Wypisz wyniki przetwarzania
    with open(output_file, 'w') as outfile:
        outfile.write("Wyniki przetwarzania formuły CNF:\n")
        outfile.write(str(model))

    # Opcjonalnie zapisz graf
    if save_graph.get() and G is not None:
        # Tutaj użyj t-SNE do osadzenia wierzchołków grafu w przestrzeni 2D
 
        
        # Tutaj dodaj kod do wizualizacji grafu na podstawie osadzenia
        plt.title("t-SNE Visualization of Graph")
        plt.show()

def open_documentation():
    # Pobierz katalog bieżący skryptu
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Utwórz ścieżkę do pliku dokumentacji w tym samym katalogu co skrypt
    documentation_path = os.path.join(script_directory, "", "dokumentacja.pdf")
    
    # Otwórz dokumentację PDF w przeglądarce internetowej
    webbrowser.open(documentation_path)
def browse_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik", filetypes=(("CNF files", "*.cnf"), ("All files", "*.*")))
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def browse_file2():
    filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    output_entry.delete(0, tk.END)
    output_entry.insert(0, filename)

def run_processing():
    input_file = file_entry.get()
    output_file = output_entry.get()
    process_data(input_file, output_file)

# Tworzenie głównego okna
root = tk.Tk()
root.title("Wizualizacja formuł logicznych")

# Wybór pliku
file_label = tk.Label(root, text="Wybierz plik CNF do przetworzenia:")
file_entry = tk.Entry(root, width=50)
file_button = tk.Button(root, text="Wybierz plik", command=browse_file)

# Wybór pliku do zapisu wyników
output_label = tk.Label(root, text="Wybierz plik do zapisu wyników:")
output_entry = tk.Entry(root, width=50)
output_button = tk.Button(root, text="Wybierz plik", command=browse_file2)

# Opcja zapisu grafu
save_graph = tk.BooleanVar()
save_graph_checkbox = tk.Checkbutton(root, text="Zapisz graf", variable=save_graph)

# Przycisk otwierający dokumentację PDF
open_doc_button = tk.Button(root, text="Otwórz dokumentację PDF", command=open_documentation)

# Przycisk uruchamiający przetwarzanie
process_button = tk.Button(root, text="Uruchom przetwarzanie", command=run_processing)

# Rozmieszczenie widgetów w oknie
file_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
file_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
file_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)
output_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
output_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
output_button.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W)
save_graph_checkbox.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
open_doc_button.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
process_button.grid(row=3, column=0, columnspan=3, pady=20)

# Uruchomienie głównej pętli programu
root.mainloop()
