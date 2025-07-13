import os
import subprocess

def git_pull_all_repos(directory):
    # Verifica se o diretório fornecido existe
    if not os.path.isdir(directory):
        print(f"Diretório {directory} não encontrado.")
        return

    # Itera sobre os subdiretórios imediatos dentro do diretório
    for repo_dir in os.listdir(directory):
        repo_path = os.path.join(directory, repo_dir)
        
        # Verifica se o subdiretório contém um repositório Git
        if os.path.isdir(repo_path) and os.path.isdir(os.path.join(repo_path, '.git')):
            print(f"Acessando repositório: {repo_dir}")
            
            # Executa o comando git pull origin
            try:
                subprocess.run(["git", "-C", repo_path, "pull", "origin"], check=True)
                print(f"git pull origin executado com sucesso no repositório {repo_dir}")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao executar git pull no repositório {repo_dir}: {e}")
        else:
            print(f"{repo_dir} não é um repositório Git válido.")

# Especifique o diretório D contendo os repositórios clonados
git_pull_all_repos("./repos")


