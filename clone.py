import csv
import os
import subprocess
import unicodedata
import re

# Nome do arquivo CSV
csv_file = 'repos.csv'

# Diretório onde os repositórios serão clonados
repos_dir = 'repos'

# Lista com repositórios que deram erro ao clonar
repos_errors = []

# Função para formatar o nome do subdiretório
def format_directory_name(full_name):
    # Divide o nome em partes
    parts = full_name.strip().split()
    if not parts:
        return "sem_nome"
    
    # Usa apenas o primeiro e o último nome
    first = parts[0]
    last = parts[-1] if len(parts) > 1 else ''
    name = f"{first}_{last}"
    
    # Remove acentos
    normalized = unicodedata.normalize('NFKD', name)
    ascii_name = normalized.encode('ASCII', 'ignore').decode('ASCII')
    
    # Remove quaisquer caracteres que não sejam letras, números ou underscores
    final_name = re.sub(r'[^\w_]', '', ascii_name)

    return final_name

# Função para clonar repositório
def clone_repository(repo_url, clone_dir):
    try:
        subprocess.run(['git', 'clone', repo_url, clone_dir], check=True)
        print(f"Repositório {repo_url} clonado em {clone_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao clonar o repositório {repo_url}: {e}")
        repos_errors.append(f"{clone_dir} : {repo_url}")

# Cria o diretório repos se não existir
if not os.path.exists(repos_dir):
    os.makedirs(repos_dir)

# Lê o arquivo CSV e clona os repositórios
with open(csv_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        full_name = row['Nome Completo']
        repo_url = row['Repositório Github']
        
        base_name = format_directory_name(full_name)
        dir_name = base_name
        clone_dir = os.path.join(repos_dir, dir_name)
        
        i = 1
        while os.path.exists(clone_dir):
            dir_name = f"{base_name}_{i}"
            clone_dir = os.path.join(repos_dir, dir_name)
            i += 1

        clone_repository(repo_url, clone_dir)

# Exibe os erros, se houver
if repos_errors:
    print("\nDeu erro ao clonar os seguintes repositórios:")
    for error in repos_errors:
        print(error)
else:
    print("\nTodos os repositórios foram clonados com sucesso.")
