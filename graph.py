#-*- coding: utf8 -*-
import tkinter as tk
from tkinter import ttk
from tkintertable import TableCanvas
from pymongo import MongoClient
import networkx as nx

client = MongoClient('localhost', 27017)
db = client["Wiki-Graph"]

g = nx.DiGraph()

all_collections = db.collection_names()
for collection in all_collections:
    for doc in db[collection].find():
        g.add_edge(collection, doc["name"])

in_degree_list = []

for item in g.nodes():
    if item.find("Glossary") == -1 and item.find("International") == -1 and item.find("Digital_object") == -1\
    and item.find("Integrated_Authority") == -1 and item.find("Wayback_Machine") ==-1 and item.find("Library_of_Congress") == -1\
    and item.find("PubMed") == -1 and item.find("National_Diet_Library") == -1 and item.find("Biblioth") == -1:
        in_degree_list.append((item, g.in_degree(item)))

in_degree_list_sorted = sorted(in_degree_list, key=lambda tup:tup[1])
top_50 = in_degree_list_sorted[len(in_degree_list_sorted)-50:len(in_degree_list_sorted)]
top_50.sort(key=lambda tup:tup[1], reverse=True)
data = {}
i = 0
for key, value in top_50:
    data[i]={"Página":key, "Qtde de referências recebida":value}
    i+=1

graph_informations={}
graph_informations["density"] = nx.density(g)
graph_informations["is_directed"] = nx.is_directed(g)
graph_informations["number_nodes"] = nx.number_of_nodes(g)
graph_informations["number_edges"] = nx.number_of_edges(g)


root = tk.Tk()
root.title("Informações do grafo")
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Top 50")
tabControl.pack(expand=1, fill="both")
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="Informações do grafo")
tabControl.pack(expand=1, fill="both")
table = TableCanvas(tab1, data=data, rowheight=20, cellwidth = 230, editable=False)
table.show()
label1 = tk.Label(tab2, pady=8, text="Tipo: " + ("Direcionado" if graph_informations["is_directed"]==True else "Não direcionado"))
label2 = tk.Label(tab2, pady=8, text="Número de nós: " + str(graph_informations["number_nodes"]))
label3 = tk.Label(tab2, pady=8, text="Número de arestas: " + str(graph_informations["number_edges"]))
label4 = tk.Label(tab2, pady=8, text="Densidade: " + str(graph_informations["density"]))
label1.pack()
label2.pack()
label3.pack()
label4.pack()
tk.mainloop()
