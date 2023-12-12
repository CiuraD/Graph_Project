import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
from sympy import symbols, to_cnf
from Methods.deep import deepWalk
from Methods.node import node2Vec
from Methods.doc import doc2Vec

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def process_data(method, input_file, output_file):
    # Wczytaj plik CNF
    cnf_formula_str = ''.join(read_file(input_file))

    # Switch dla różnych możliwych wyborów
    if method == "Deep Walk":
        G,model,time = deepWalk(input_file)
        
    elif method == "Node2Vec":
        G,model,time = node2Vec(input_file)


        

    elif method == "Doc2Vec":
        G,model,time = doc2Vec(input_file)

    else:
        print("Nieznana metoda")


    # Wypisz wyniki przetwarzania
    with open(output_file, 'w') as outfile:
        outfile.write("Wyniki przetwarzania formuły CNF:\n")
        outfile.write(f"Formuła wejściowa: {cnf_formula_str}\n")
     

    # Opcjonalnie zapisz graf
    if save_graph.get():
        G = nx.Graph()
        # Tutaj dodaj kod do tworzenia grafu na podstawie przetworzonej formuły
        nx.draw(G, with_labels=True)
        plt.savefig('graph.png')
        plt.show()

def browse_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik", filetypes=(("CNF files", "*.cnf"), ("All files", "*.*")))
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def browse_file2():
    filename = filedialog.askopenfilename(initialdir="/",title="Wybierz plik",filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    output_entry.delete(0, tk.END)
    output_entry.insert(0, filename)

def run_processing():
    method = method_var.get()
    input_file = file_entry.get()
    output_file = output_entry.get()
    process_data(method, input_file, output_file)

# Tworzenie głównego okna
root = tk.Tk()
root.title("Wizualizacja formuł logicznych")

# Wybór metody
method_var = tk.StringVar()
method_var.set("Deep Walk")

method_label = tk.Label(root, text="Wybierz metodę:")
method_menu = tk.OptionMenu(root, method_var, "Deep Walk", "Node2Vec", "Doc2Vec")

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

# Przycisk uruchamiający przetwarzanie
process_button = tk.Button(root, text="Uruchom przetwarzanie", command=run_processing)

# Rozmieszczenie widgetów w oknie
method_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
method_menu.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
file_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
file_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
file_button.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W)
output_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
output_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
output_button.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
save_graph_checkbox.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
process_button.grid(row=4, column=0, columnspan=3, pady=20)

# Uruchomienie głównej pętli programu
root.mainloop()
