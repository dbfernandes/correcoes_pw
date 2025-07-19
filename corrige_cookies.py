import os
import re

def find_resource_directory(base_dir):
    possibilities = [
        "src/resources/products", 
        "src/resource/product", 
        "src/resources/product", 
        "src/resource/products"
    ]
    for path in possibilities:
        full_path = os.path.join(base_dir, path)
        if os.path.isdir(full_path):
            return full_path
    return None

def find_file_by_keyword(resource_dir, keyword):
    for fname in os.listdir(resource_dir):
        full_path = os.path.join(resource_dir, fname)
        if os.path.isfile(full_path) and keyword.lower() in fname.lower():
            return full_path
    return None

def check_type_file(type_file):
    with open(type_file, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    has_create = re.search(r'type\s+\w*create\w*', content)
    has_update = re.search(r'type\s+\w*update\w*', content)
    return bool(has_create) and bool(has_update)

def check_schema_file(schema_file):
    with open(schema_file, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    return "joi.object" in content

def check_router_file(router_file, schema_filename):
    with open(router_file, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    methods_ok = all(method in content for method in ['router.get', 'router.post', 'router.put', 'router.delete'])
    schema_name = os.path.splitext(os.path.basename(schema_filename))[0].lower() if schema_filename else ''
    imports_schema = schema_name in content
    return methods_ok and imports_schema

def check_service_file(service_file):
    with open(service_file, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    return all(k in content for k in ['prisma', 'find', 'create', 'update', 'delete'])

def check_controller_file(controller_file):
    with open(controller_file, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    funcs = ['create', 'index', 'read', 'update', 'remove']
    functions_ok = all(re.search(rf'\b{fn}\b', content) for fn in funcs)
    uses_res = 'res.' in content
    return functions_ok and uses_res

def analyze_express_project(base_dir):
    resource_dir = find_resource_directory(base_dir)
    if not resource_dir:
        print("  ❌ Diretório de resources não encontrado.")
        return

    keywords = ['controller', 'router', 'schema', 'service', 'type']
    file_paths = {k: find_file_by_keyword(resource_dir, k) for k in keywords}

    for k in keywords:
        path = file_paths[k]
        if path:
            print(f"  ✅ Arquivo *{k}* encontrado: {os.path.basename(path)}")
        else:
            print(f"  ❌ Arquivo *{k}* não encontrado.")
            continue

        try:
            if k == 'type':
                ok = check_type_file(path)
                print(f"    └─ ✔️ Types 'create' e 'update' presentes." if ok else "    └─ ❌ Types esperados ausentes.")
            elif k == 'schema':
                ok = check_schema_file(path)
                print(f"    └─ ✔️ Validação com Joi presente." if ok else "    └─ ❌ Joi.object não encontrado.")
            elif k == 'router':
                ok = check_router_file(path, file_paths['schema'])
                print(f"    └─ ✔️ Rotas e importação do schema OK." if ok else "    └─ ❌ Rotas incompletas ou schema não importado.")
            elif k == 'service':
                ok = check_service_file(path)
                print(f"    └─ ✔️ Uso esperado do Prisma OK." if ok else "    └─ ❌ Uso esperado do Prisma ausente.")
            elif k == 'controller':
                ok = check_controller_file(path)
                print(f"    └─ ✔️ Funções com 'res' estão presentes." if ok else "    └─ ❌ Funções ausentes ou sem resposta com 'res'.")
        except Exception as e:
            print(f"    └─ ⚠️ Erro ao analisar arquivo {k}: {e}")

def avaliar_todos_os_alunos(diretorio_turma):
    for aluno in sorted(os.listdir(diretorio_turma)):
        path_aluno = os.path.join(diretorio_turma, aluno)
        if not os.path.isdir(path_aluno):
            continue

        print(f"\n🧑 Avaliando: {aluno}")

        # Procurar diretório com "WACAD011" ou "COOKIE"
        subdir = next((d for d in os.listdir(path_aluno)
                       if re.search(r'(WACAD011|COOKIE)', d, re.IGNORECASE)), None)
        if not subdir:
            print("  ❌ Subdiretório com 'WACAD011' ou 'COOKIE' não encontrado.")
            continue

        path_subdir = os.path.join(path_aluno, subdir)

        # Procurar subdiretório com "exp"
        subexp = next((d for d in os.listdir(path_subdir)
                       if 'exp' in d.lower() and os.path.isdir(os.path.join(path_subdir, d))), None)
        if not subexp:
            print("  ❌ Subdiretório com 'exp' não encontrado.")
            continue

        path_expapi = os.path.join(path_subdir, subexp)

        # Rodar verificação da aplicação Express
        analyze_express_project(path_expapi)

# 🟢 Altere o caminho abaixo conforme necessário
if __name__ == "__main__":
    avaliar_todos_os_alunos("./reposTF")

