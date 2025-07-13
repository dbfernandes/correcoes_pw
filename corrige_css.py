import os
import re
import subprocess

def abrir_htmls_em_janelas_por_aluno(diretorio_raiz: str):
    # Alunos em ordem alfabética decrescente
    alunos = sorted(os.listdir(diretorio_raiz), key=str.lower, reverse=True)

    for aluno in alunos:
        caminho_aluno = os.path.join(diretorio_raiz, aluno)
        if not os.path.isdir(caminho_aluno):
            continue

        # Encontrar subdiretório que contenha "wacad002" (case-insensitive)
        subdirs_wacad = [
            d for d in os.listdir(caminho_aluno)
            if os.path.isdir(os.path.join(caminho_aluno, d)) and
               re.search(r'wacad002', d, re.IGNORECASE)
        ]
        if not subdirs_wacad:
            continue  # pula aluno

        dir_wacad = os.path.join(caminho_aluno, subdirs_wacad[0])

        # Coletar todos os arquivos .html dentro de wacad002 e subpastas
        arquivos_html = []
        for root, _, files in os.walk(dir_wacad):
            for file in sorted(files, key=str.lower):
                if file.lower().endswith('.html'):
                    caminho_html = os.path.join(root, file)
                    arquivos_html.append(caminho_html)

        if arquivos_html:
            print(f"Abrindo {len(arquivos_html)} arquivos para aluno {aluno}...")
            subprocess.Popen(["google-chrome", "--new-window"] + arquivos_html)

# Executar
abrir_htmls_em_janelas_por_aluno("repos/")
