import numpy as np

def extract_classes_from_ptc(ptc_file):
    # Abrir o arquivo PTC
    with open(ptc_file, 'r') as file:
        lines = file.readlines()

    classes = []
    
    # Iterar pelas linhas do arquivo PTC
    for line in lines:
        if line.startswith('POINT'):
            # Extrair a classe do ponto
            class_start_index = line.find('CLASS') + 6
            class_end_index = line.find(' ', class_start_index)
            class_value = int(line[class_start_index:class_end_index])
            
            # Adicionar a classe à lista
            classes.append(class_value)
    
    return classes

# Exemplo de uso
ptc_file_path = input("Digite o caminho do arquivo PTC: ")
class_list = extract_classes_from_ptc(ptc_file_path)

# Imprimir as classes extraídas
for i, class_value in enumerate(class_list):
    print(f"Ponto {i+1}: Classe {class_value}")
