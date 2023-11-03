import unicodedata
import csv
import networkx as nx
import matplotlib.pyplot as plt
import string
import re

from utils import word_dict

def remover_acentuacao(texto):
    
    nfkd = unicodedata.normalize('NFKD', texto)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usar expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

def process_message(msg):
    special_chars = string.punctuation
    text = str(msg).lower()
    text = re.sub(f"[{special_chars}]", "", text)
    text = remover_acentuacao(text)

    return text

word_dict_clear = {k: remover_acentuacao(v).strip() for k, v in word_dict.items()}
word_list = [{'word': word, 'id': _id} for _id, word in word_dict_clear.items()]

G = nx.Graph()

for word in word_list:
    G.add_node(word['id'])


with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Pular o cabeçalho

    for row in reader:
        node_id = row[1]
        G.add_node(node_id)

        # Obter a frase e o ID da palavra
        frase = process_message(row[0])
        
        for words in word_list:
            word_id = words['id']
            word = words['word'].lower()
            #print(word, frase)
            if word in frase:
                G.add_edge(node_id, word_id)  # Adicionar uma aresta entre o nó e a palavra


degree_centrality = nx.degree_centrality(G)
# centralidade geral média de grau
average_degree_centrality = sum(degree_centrality.values()) / len(degree_centrality)
print("Centralidade Geral Média de Grau:", average_degree_centrality)

betweenness_centrality = nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
# Betweeness média
average_betweenness_centrality = sum(betweenness_centrality.values()) / len(betweenness_centrality)
print("Betweeness:", average_betweenness_centrality)


closeness_centrality = nx.closeness_centrality(G, u=None, distance=None, wf_improved=True)
# closeness média
average_closeness_centrality = sum(closeness_centrality.values()) / len(closeness_centrality)
print("closeness:", average_closeness_centrality)

max_diameter = 0
components = list(nx.connected_components(G))
for component in components:
    subgraph = G.subgraph(component)
    diameter = nx.diameter(subgraph)
    if(diameter > max_diameter ):
        max_diameter = diameter

print(f"Diâmetro do componente: {max_diameter}")


clustering = nx.clustering(G, nodes=None, weight=None)
average_clustering = sum(clustering.values()) / len(clustering)

print(f"clusterinf coeficient: {average_clustering}")

print('plotando o grafo como imagem....')

plt.figure(2)
nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels=True,  )
plt.show()
           


