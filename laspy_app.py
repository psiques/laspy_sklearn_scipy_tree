import laspy
import numpy as np
from scipy.spatial import KDTree
from sklearn.cluster import KMeans
import pandas as pd

"""Função para rotular as classes"""

def rotular_classe(valor):
    if valor == 0:
        return "Zero length line"
    elif valor == 1:
        return "Chão"
    elif valor == 2:
        return "Vegetação Baixa"
    elif valor == 3:
        return "Vegetação Média"
    elif valor == 4:
        return "Vegetação Alta"
    elif valor == 5:
        return "Prédios"
    elif valor == 6:
        return "Terraço ou Telhado"
    elif valor == 7:
        return "Rio/Lago navegável"
    elif valor == 8:
        return "Rio/Lago não navegável"
    elif valor == 9:
        return "Ferrovias"
    elif valor == 10:
        return "Rua - Tipo 1"
    elif valor == 11:
        return "Rua - Tipo 2"
    elif valor == 12:
        return "Rua - Tipo 3"
    elif valor == 13:
        return "Rua - Tipo 4"
    elif valor == 14:
        return "Ponte"
    elif valor == 15:
        return "Condutores nus"
    elif valor == 16:
        return "Cabos aéreos Elicord"
    elif valor == 17:
        return "Postes"
    elif valor == 18:
        return "Linhas aéreas HV"
    elif valor == 19:
        return "Linhas aéreas MV"
    elif valor == 20:
        return "Linhas aéreas LV"
    elif valor == 21:
        return "Linhas aéreas de outros tipos"
    elif valor == 22:
        return "Cabos diversos"
    elif valor == 23:
        return "Interferência de Vegetação_1"
    elif valor == 24:
        return "Interferência de Vegetação_2"
    elif valor == 25:
        return "Interferência de Vegetação_3"
    elif valor == 26:
        return "Interferência entre cabos_1"
    elif valor == 27:
        return "Interferência entre cabos_2"
    elif valor == 28:
        return "Interferência entre cabos_3"
    elif valor == 29:
        return "Interferência de Edificação_1"
    elif valor == 30:
        return "Interferência de Edificação_2"
    elif valor == 31:
        return "Interferência de Edificação_3"
    elif valor == 32:
        return "Model Keypoints"
    elif valor == 33:
        return "Default"
    elif valor == 34:
        return "Low point"
    else:
        return "Classe não identificada"

"""Abrir e ler o arquivo LAS/LAZ:"""

file_path = input("Digite o caminho do arquivo LAS/LAZ: ")
infile = laspy.read(file_path)
infile

points = np.vstack((infile.x, infile.y, infile.z)).transpose()

"""Filtrar as classes de vegetação e interferência da vegetação e aplicar a clusterização:"""

vegetation_classes = [2, 3, 4, 23, 24, 25]  # Classes de vegetação e interferência da vegetação

filtered_points = points[np.isin(infile.classification, vegetation_classes)]
filtered_coordinates = filtered_points[:, :3]

num_trees = int(input("Digite o número estimado de árvores: "))
kmeans = KMeans(n_clusters=num_trees, n_init=10, random_state=0).fit(filtered_coordinates)
tree_labels = kmeans.labels_

min_z = np.min(filtered_points[:, 2])
heights = filtered_points[:, 2] - min_z

tree_ids = np.arange(1, num_trees + 1)
tree_heights = []
for tree_id in tree_ids:
    tree_height = np.max(heights[filtered_points[:, 0] == tree_id])
    tree_heights.append((tree_id, tree_height))

# Imprimir informações
for tree_labels, tree_height in tree_heights:
    print(f"ID: {tree_labels}, Altura: {tree_height}")

import matplotlib.pyplot as plt

# Supondo que você tenha as coordenadas x, y e as labels das árvores segmentadas

# Plotando as árvores segmentadas
for i in range(num_trees):
    tree_points = filtered_points[tree_labels == i]
    x = tree_points[:, 0]  # Coordenada x dos pontos
    y = tree_points[:, 1]  # Coordenada y dos pontos
    plt.scatter(x, y)

plt.xlabel("Coordenada x")
plt.ylabel("Coordenada y")
plt.title("Árvores Segmentadas")
plt.show()

x = filtered_points[:, 0]  # Coordenada x dos pontos
y = filtered_points[:, 1]  # Coordenada y dos pontos
z = filtered_points[:, 2]  # Coordenada z dos pontos

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z)
ax.set_xlabel('Coordenada X')
ax.set_ylabel('Coordenada Y')
ax.set_zlabel('Coordenada Z')
plt.title('Árvores Segmentadas')
plt.show()

# Salvando as informações em uma tabela XLS
data = {'Tree ID': [], 'Height': [], 'Class': []}
for tree_id, tree_height in tree_heights:
    class_value = infile.classification[filtered_points[:, 0] == tree_id][0]
    class_label = rotular_classe(class_value)
    data['Tree ID'].append(tree_id)
    data['Height'].append(tree_height)
    data['Class'].append(class_label)

df = pd.DataFrame(data)
output_file = input("Digite o caminho e nome do arquivo XLS de saída: ")
df.to_excel(output_file, index=False)
print("Arquivo XLS salvo com sucesso!")
