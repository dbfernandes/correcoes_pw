import os
import re
from bs4 import BeautifulSoup

# Exercício 1
def corrigir_exercicio_1(html: str) -> tuple[float, str]:
    soup = BeautifulSoup(html, 'html.parser')
    nota = 0
    problemas = []

    if any(soup.find(tag) for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        nota += 1
    else:
        problemas.append("- Não foi encontrada nenhuma tag de título (h1 a h6).")

    if soup.find('strong') or soup.find('b'):
        nota += 1
    else:
        problemas.append("- Não foi encontrado texto em negrito (<strong> ou <b>).")

    if soup.find('em') or soup.find('i'):
        nota += 1
    else:
        problemas.append("- Não foi encontrado texto em itálico (<em> ou <i>).")

    if soup.find('img'):
        nota += 1
    else:
        problemas.append("- Não foi encontrada nenhuma imagem (<img>).")

    if soup.find('pre'):
        nota += 1
    else:
        problemas.append("- Não foi encontrado bloco de código com a tag <pre>.")

    if soup.find('sub') and soup.find('sup') and soup.find('small'):
        nota += 1
    else:
        faltando = []
        if not soup.find('sub'): faltando.append("<sub>")
        if not soup.find('sup'): faltando.append("<sup>")
        if not soup.find('small'): faltando.append("<small>")
        problemas.append(f"- Faltam as seguintes tags: {', '.join(faltando)}.")

    nota_final = round((nota / 6) * 10, 2)
    relatorio = "\n".join(problemas) if problemas else "- Todos os elementos obrigatórios foram encontrados."
    return nota_final, relatorio

# Exercício 2
def corrigir_exercicio_2(html: str) -> tuple[float, str]:
    soup = BeautifulSoup(html, 'html.parser')
    nota = 0
    problemas = []

    if any(soup.find(tag) for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        nota += 3
    else:
        problemas.append("- Nenhuma tag de título (h1 a h6) foi encontrada.")

    tabela = soup.find('table')
    if tabela:
        nota += 3
        encontrou_span = any(tag.has_attr('colspan') or tag.has_attr('rowspan') for tag in tabela.find_all(['td', 'th']))
        if encontrou_span:
            nota += 4
        else:
            problemas.append("- Nenhum uso de colspan ou rowspan foi encontrado na tabela.")
    else:
        problemas.append("- Nenhuma tabela (<table>) foi encontrada.")

    nota_final = round(nota, 2)
    relatorio = "\n".join(problemas) if problemas else "- Todos os elementos obrigatórios foram encontrados."
    return nota_final, relatorio

# Exercício 3
def corrigir_exercicio_3(html: str) -> tuple[float, str]:
    soup = BeautifulSoup(html, 'html.parser')
    nota = 0
    problemas = []

    tags_requeridas = ['header', 'nav', 'main', 'article', 'figure', 'p', 'section', 'aside', 'footer']

    for tag in tags_requeridas:
        if soup.find(tag):
            nota += 1
        else:
            problemas.append(f"- A tag <{tag}> não foi encontrada.")

    nota_final = round((nota / len(tags_requeridas)) * 10, 2)
    relatorio = "\n".join(problemas) if problemas else "- Todas as tags semânticas foram encontradas."
    return nota_final, relatorio

# Exercício 4
def corrigir_exercicio_4(html: str) -> tuple[float, str]:
    soup = BeautifulSoup(html, 'html.parser')
    nota = 0
    problemas = []

    if soup.find('input', {'type': 'text'}):
        nota += 1
    else:
        problemas.append("- Nenhum <input type='text'> encontrado.")

    if soup.find('input', {'type': 'radio'}):
        nota += 1
    else:
        problemas.append("- Nenhum <input type='radio'> encontrado.")

    if soup.find('input', {'type': 'checkbox'}):
        nota += 1
    else:
        problemas.append("- Nenhum <input type='checkbox'> encontrado.")

    if soup.find('fieldset') and soup.find('legend'):
        nota += 1
    else:
        problemas.append("- <fieldset> e/ou <legend> não encontrados.")

    if soup.find('textarea'):
        nota += 1
    else:
        problemas.append("- Nenhum <textarea> encontrado.")

    select = soup.find('select')
    if select and select.find('option'):
        nota += 1
    else:
        problemas.append("- Nenhum <select> com <option> encontrado.")

    tem_botao = soup.find('button') or \
                soup.find('input', {'type': 'submit'}) or \
                soup.find('input', {'type': 'reset'})

    if tem_botao:
        nota += 1
    else:
        problemas.append("- Nenhum botão foi encontrado (<button>, <input type='submit'> ou <input type='reset'>).")

    nota_final = round((nota / 7) * 10, 2)
    relatorio = "\n".join(problemas) if problemas else "- Todos os elementos de formulário foram encontrados."
    return nota_final, relatorio


# Função auxiliar
def encontrar_html_em_pasta(base_dir: str, substrings: list[str]) -> str | None:
    for subdir in os.listdir(base_dir):
        caminho_subdir = os.path.join(base_dir, subdir)
        if os.path.isdir(caminho_subdir):
            nome_lower = subdir.lower()
            if all(sub in nome_lower for sub in substrings):
                arquivos_html = [f for f in os.listdir(caminho_subdir) if f.lower().endswith('.html')]
                if arquivos_html:
                    return os.path.join(caminho_subdir, arquivos_html[0])
    return None

# Avaliação principal
def avaliar_htmls_de_alunos(diretorio_raiz: str):
    for aluno in sorted(os.listdir(diretorio_raiz), key=str.lower):
        caminho_aluno = os.path.join(diretorio_raiz, aluno)
        if not os.path.isdir(caminho_aluno):
            continue

        subdirs_wacad = [
            d for d in os.listdir(caminho_aluno)
            if os.path.isdir(os.path.join(caminho_aluno, d)) and
            re.search(r'wacad001', d, re.IGNORECASE)
        ]
        if not subdirs_wacad:
            continue

        dir_wacad = os.path.join(caminho_aluno, subdirs_wacad[0])

        print(f"\nAluno: {aluno}")
        print("=" * 60)

        # Exercício 1
        caminho_html1 = encontrar_html_em_pasta(dir_wacad, ["html", "1"])
        if caminho_html1:
            try:
                with open(caminho_html1, 'r', encoding='utf-8') as f:
                    html1 = f.read()
                nota1, relatorio1 = corrigir_exercicio_1(html1)
                print("[Exercício 1]")
                print(f"Nota: {nota1}/10")
                print("Correções:")
                print(relatorio1)
            except Exception as e:
                print(f"[Exercício 1] Erro ao processar: {e}")
        else:
            print("[Exercício 1] ❌ Arquivo HTML não encontrado.")

        print()

        # Exercício 2
        caminho_html2 = encontrar_html_em_pasta(dir_wacad, ["html", "2"])
        if caminho_html2:
            try:
                with open(caminho_html2, 'r', encoding='utf-8') as f:
                    html2 = f.read()
                nota2, relatorio2 = corrigir_exercicio_2(html2)
                print("[Exercício 2]")
                print(f"Nota: {nota2}/10")
                print("Correções:")
                print(relatorio2)
            except Exception as e:
                print(f"[Exercício 2] Erro ao processar: {e}")
        else:
            print("[Exercício 2] ❌ Arquivo HTML não encontrado.")

        print()

        # Exercício 3
        caminho_html3 = encontrar_html_em_pasta(dir_wacad, ["html", "3"])
        if caminho_html3:
            try:
                with open(caminho_html3, 'r', encoding='utf-8') as f:
                    html3 = f.read()
                nota3, relatorio3 = corrigir_exercicio_3(html3)
                print("[Exercício 3]")
                print(f"Nota: {nota3}/10")
                print("Correções:")
                print(relatorio3)
            except Exception as e:
                print(f"[Exercício 3] Erro ao processar: {e}")
        else:
            print("[Exercício 3] ❌ Arquivo HTML não encontrado.")

        print()

        # Exercício 4
        caminho_html4 = encontrar_html_em_pasta(dir_wacad, ["html", "4"])
        if caminho_html4:
            try:
                with open(caminho_html4, 'r', encoding='utf-8') as f:
                    html4 = f.read()
                nota4, relatorio4 = corrigir_exercicio_4(html4)
                print("[Exercício 4]")
                print(f"Nota: {nota4}/10")
                print("Correções:")
                print(relatorio4)
            except Exception as e:
                print(f"[Exercício 4] Erro ao processar: {e}")
        else:
            print("[Exercício 4] ❌ Arquivo HTML não encontrado.")

        print("=" * 60)

# Executar
avaliar_htmls_de_alunos("repos/")
