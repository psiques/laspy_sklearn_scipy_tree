import laspy
import numpy as np
from scipy.spatial import KDTree
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt

    # Código de rotulação de classes
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
  
file_path = input("Digite o caminho do arquivo LAS/LAZ: ")
infile = laspy.read(file_path)

points = np.vstack((infile.x, infile.y, infile.z)).transpose()

vegetation_classes = [2, 3, 4, 23, 24, 25]

filtered_points = points[np.isin(infile.classification, vegetation_classes)]
filtered_coordinates = filtered_points[:, :3]

num_trees = int(input("Digite o número estimado de árvores: "))
kmeans = KMeans(n_clusters=num_trees, random_state=0).fit(filtered_coordinates)
tree_labels = kmeans.labels_

min_z = np.min(filtered_points[:, 2])
heights = filtered_points[:, 2] - min_z

tree_ids = np.unique(tree_labels)
tree_heights = []
for tree_id in tree_ids:
    tree_points_tree_id = tree_labels == tree_id
    if np.any(tree_points_tree_id):
        tree_height = np.max(heights[tree_points_tree_id])
        tree_heights.append((tree_id, tree_height))

# Criar DataFrame com os dados das árvores segmentadas
data = {'Tree ID': [], 'Height': [], 'Class': []}
for tree_id, tree_height in tree_heights:
    tree_points = filtered_points[tree_labels == tree_id]
    class_value = np.unique(infile.classification[tree_labels == tree_id])[0]
    class_label = rotular_classe(int(class_value))
    data['Tree ID'].append(tree_id)
    data['Height'].append(tree_height)
    data['Class'].append(class_label)

df = pd.DataFrame(data)

# Salvar DataFrame em arquivo XLS
output_file = input("Digite o caminho e nome do arquivo XLS de saída: ")
df.to_excel(output_file, index=False)
print("Arquivo XLS salvo com sucesso!")

# Plotando as árvores segmentadas
fig, ax = plt.subplots()
for i in range(num_trees):
    tree_points = filtered_points[tree_labels == i]
    x = tree_points[:, 0]  # Coordenada x dos pontos
    y = tree_points[:, 1]  # Coordenada y dos pontos
    ax.scatter(x, y)

ax.set_xlabel("Coordenada x")
ax.set_ylabel("Coordenada y")
ax.set_title("Árvores Segmentadas")
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(filtered_points[:, 0], filtered_points[:, 1], filtered_points[:, 2])
ax.set_xlabel('Coordenada X')
ax.set_ylabel('Coordenada Y')
ax.set_zlabel('Coordenada Z')
plt.title('Árvores Segmentadas')
plt.show()

# Exportar arquivo LAS segmentado das árvores
outfile_path = input("Digite o caminho e nome do arquivo LAS segmentado de saída: ")
outfile = laspy.file.File(outfile_path, mode="w", header=infile.header)
outfile.points = laspy.util.PointFormat().pack(
    x=filtered_points[:, 0],
    y=filtered_points[:, 1],
    z=filtered_points[:, 2],
    intensity=infile.intensity[tree_labels == tree_id],
    classification=infile.classification[tree_labels == tree_id],
    scan_angle_rank=infile.scan_angle_rank[tree_labels == tree_id],
    user_data=infile.user_data[tree_labels == tree_id],
    pt_src_id=infile.pt_src_id[tree_labels == tree_id]
)
outfile.close()

print("Arquivo LAS segmentado das árvores exportado com sucesso!")
