
import os
import re

def read_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().lower()
    except:
        return ""

def count_lines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0

def find_file_by_keyword(resource_dir, keyword):
    for fname in os.listdir(resource_dir):
        full_path = os.path.join(resource_dir, fname)
        if os.path.isfile(full_path) and keyword.lower() in fname.lower():
            return full_path
    return None

def find_resource_directory_with_substring(base_dir, substring):
    for root, dirs, _ in os.walk(os.path.join(base_dir, 'src')):
        for d in dirs:
            if 'resource' in root.lower() and substring.lower() in d.lower():
                return os.path.join(root, d)
    return None

def find_middleware_directory(base_dir):
    for root, dirs, _ in os.walk(os.path.join(base_dir, 'src')):
        for d in dirs:
            if 'middleware' in d.lower():
                return os.path.join(root, d)
    return None



def verify_lang_resource(base_dir):
    results = []
    lang_resource = find_resource_directory_with_substring(base_dir, 'lang')
    if not lang_resource:
        return ["❌ Resource 'lang*' não encontrado."]
    results.append("✅ Resource 'lang*' encontrado.")

    controller_file = find_file_by_keyword(lang_resource, 'controller')
    if controller_file:
        content = read_file_content(controller_file)
        if 'res.cookie' in content:
            results.append("  ✔️ res.cookie encontrado no controller de lang.")
        else:
            results.append("  ❌ res.cookie não encontrado no controller de lang.")
    else:
        results.append("  ❌ Arquivo controller não encontrado no resource lang.")

    middleware_dir = find_middleware_directory(base_dir)
    if middleware_dir:
        found_cookie = False
        for fname in os.listdir(middleware_dir):
            content = read_file_content(os.path.join(middleware_dir, fname))
            if 'req.cookies' in content and 'res.cookie' in content:
                found_cookie = True
                break
        if found_cookie:
            results.append("  ✔️ Middleware usa req.cookies e res.cookie.")
        else:
            results.append("  ❌ Middleware não usa req.cookies e res.cookie.")
    else:
        results.append("  ❌ Diretório middleware não encontrado.")
    return results

def verify_prisma_schema(base_dir):
    results = []
    schema_path = os.path.join(base_dir, 'prisma', 'schema.prisma')
    if not os.path.isfile(schema_path):
        return ["❌ Arquivo prisma/schema.prisma não encontrado."]
    results.append("✅ Arquivo prisma/schema.prisma encontrado.")
    content = read_file_content(schema_path)
    expected_models = ['product', 'user', 'usuario', 'type', 'tipo', 'compra', 'purchase']
    for model in expected_models:
        if model.lower() in content:
            results.append(f"  ✔️ Modelo com '{model}' encontrado.")
        else:
            results.append(f"  ❌ Modelo com '{model}' não encontrado.")
    return results

def verify_seed_file(base_dir):
    results = []
    prisma_dir = os.path.join(base_dir, 'prisma')
    if not os.path.isdir(prisma_dir):
        return ["❌ Diretório prisma/ não encontrado."]
    for fname in os.listdir(prisma_dir):
        if 'seed' in fname.lower() or 'semente' in fname.lower():
            content = read_file_content(os.path.join(prisma_dir, fname))
            if 'createmany' in content and 'disconnect' in content:
                return ["✅ Arquivo de seed encontrado com prisma.createMany e prisma.disconnect."]
            else:
                return ["❌ Arquivo de seed encontrado, mas faltam prisma.createMany ou prisma.disconnect."]
    return ["❌ Arquivo de seed/seed.ts não encontrado."]



def verify_user_resource(base_dir):
    results = []
    user_resource = find_resource_directory_with_substring(base_dir, 'user') or find_resource_directory_with_substring(base_dir, 'usuario')
    if not user_resource:
        return ["❌ Resource 'user' ou 'usuario' não encontrado."]
    results.append("✅ Resource 'user' ou 'usuario' encontrado.")

    type_file = find_file_by_keyword(user_resource, 'type') or find_file_by_keyword(user_resource, 'tipo')
    if type_file:
        content = read_file_content(type_file)
        if 'create' in content and 'update' in content:
            results.append("  ✔️ Arquivo type/tipo possui 'create' e 'update'.")
        else:
            results.append("  ❌ Arquivo type/tipo não possui 'create' ou 'update'.")
    else:
        results.append("  ❌ Arquivo type/tipo não encontrado.")

    service_file = find_file_by_keyword(user_resource, 'service') or find_file_by_keyword(user_resource, 'servico')
    if service_file:
        content = read_file_content(service_file)
        prisma_keywords = ['create', 'find', 'update', 'delete']
        if all(k in content for k in prisma_keywords):
            results.append("  ✔️ Service usa prisma.create/find/update/delete.")
        else:
            results.append("  ❌ Service não usa todas funções esperadas do prisma.")
        extra_keywords = ['bcryptjs', 'gensalt', 'process.env', 'compare']
        for kw in extra_keywords:
            if kw in content:
                results.append(f"  ✔️ '{kw}' encontrado no service.")
            else:
                results.append(f"  ❌ '{kw}' não encontrado no service.")
    else:
        results.append("  ❌ Arquivo service/servico não encontrado.")
    return results

def verify_middlewares(base_dir):
    results = []
    middleware_dir = find_middleware_directory(base_dir)
    if not middleware_dir:
        return ["❌ Diretório middleware* não encontrado."]
    for name in ['isAdmin.ts', 'isAuth.ts']:
        path = os.path.join(middleware_dir, name)
        if os.path.isfile(path):
            content = read_file_content(path)
            if 'req.session' in content and 'next' in content:
                results.append(f"  ✔️ {name} possui req.session e next.")
            else:
                results.append(f"  ❌ {name} não possui req.session ou next.")
        else:
            results.append(f"  ❌ {name} não encontrado.")
    return results



def verify_purchase_resource_extra(base_dir):
    results = []
    purchase_resource = find_resource_directory_with_substring(base_dir, 'purchase') or find_resource_directory_with_substring(base_dir, 'compra')
    if not purchase_resource:
        return ["❌ Resource 'purchase' ou 'compra' não encontrado."]
    results.append("✅ Resource 'purchase' ou 'compra' encontrado.")

    controller = find_file_by_keyword(purchase_resource, 'controller')
    service = find_file_by_keyword(purchase_resource, 'service')
    router = find_file_by_keyword(purchase_resource, 'router')
    schema = find_file_by_keyword(purchase_resource, 'schema')
    types = find_file_by_keyword(purchase_resource, 'type')

    if service:
        content = read_file_content(service)
        if 'prisma' in content and 'create' in content:
            results.append("  ✔️ Service possui prisma.create.")
        else:
            results.append("  ❌ Service não possui prisma.create.")
    else:
        results.append("  ❌ Arquivo service não encontrado.")

    if controller and service:
        total_lines = count_lines(controller) + count_lines(service)
        if total_lines >= 150:
            results.append(f"  ✔️ controller + service tem {total_lines} linhas (>= 150).")
        else:
            results.append(f"  ❌ controller + service tem {total_lines} linhas (< 150).")
    else:
        results.append("  ❌ controller ou service não encontrados para contar linhas.")

    if router:
        content = read_file_content(router)
        if all(method in content for method in ['get', 'post', 'put', 'delete']):
            results.append("  ✔️ Router possui todos os métodos (GET, POST, PUT, DELETE).")
        else:
            results.append("  ❌ Router não possui todos os métodos esperados.")
    else:
        results.append("  ❌ Arquivo router não encontrado.")

    if schema:
        content = read_file_content(schema)
        if 'joi.object' in content:
            results.append("  ✔️ Schema possui Joi.object.")
        else:
            results.append("  ❌ Schema não possui Joi.object.")
    else:
        results.append("  ❌ Arquivo schema não encontrado.")

    if types:
        lines = count_lines(types)
        if lines > 15:
            results.append(f"  ✔️ Type possui {lines} linhas (> 15).")
        else:
            results.append(f"  ❌ Type possui apenas {lines} linhas (<= 15).")
    else:
        results.append("  ❌ Arquivo type não encontrado.")
    return results

def verify_controller_swagger_summary(base_dir, resource_name):
    results = []
    resource = find_resource_directory_with_substring(base_dir, resource_name)
    if not resource:
        return [f"❌ Resource '{resource_name}' não encontrado."]
    controller = find_file_by_keyword(resource, 'controller')
    if not controller:
        return [f"❌ Controller do resource '{resource_name}' não encontrado."]
    print(resource_name)
    print("KKKKKKKKKKKKKKKKK")
    content = read_file_content(controller)
    func_names = re.findall(r'const\s+(\w+)\s*(?::[^=]+)?=\s*async\s*\(', content)
    print(func_names)
    for name in func_names:
        if f'{name}' in content and 'swagger.summary' in content:
            results.append(f"  ✔️ Função {name} possui swagger.summary.")
        else:
            results.append(f"  ❌ Função {name} não possui swagger.summary.")
    return results

def verify_swagger_root(base_dir):
    results = []
    swagger_file = os.path.join(base_dir, 'src', 'swagger.ts')
    if os.path.isfile(swagger_file):
        results.append("✅ Arquivo swagger.ts encontrado na raiz.")
    else:
        results.append("❌ Arquivo swagger.ts não encontrado na raiz.")

    router_dir = os.path.join(base_dir, 'src', 'router')
    count = 0
    if os.path.isdir(router_dir):
        for fname in os.listdir(router_dir):
            path = os.path.join(router_dir, fname)
            content = read_file_content(path)
            count += content.count('swagger.tags')
        results.append(f"✔️ swagger.tags aparece {count} vez(es) em arquivos de /router.")
    else:
        results.append("❌ Diretório /router não encontrado.")
    return results





def avaliar_todos_os_alunos(diretorio_turma):
    for aluno in sorted(os.listdir(diretorio_turma)):
        path_aluno = os.path.join(diretorio_turma, aluno)
        if not os.path.isdir(path_aluno):
            continue

        print(f"\n🧑 Avaliando: {aluno}")

        subdir = next((d for d in os.listdir(path_aluno)
                       if re.search(r'(WACAD013|API)', d, re.IGNORECASE)), None)
        if not subdir:
            print("  ❌ Subdiretório com 'WACAD013' ou 'API' não encontrado.")
            continue

        path_subdir = os.path.join(path_aluno, subdir)

        subexp = next((d for d in os.listdir(path_subdir)
                       if 'exp' in d.lower() and os.path.isdir(os.path.join(path_subdir, d))), None)
        if not subexp:
            print("  ❌ Subdiretório com 'exp' não encontrado.")
            continue

        path_expapi = os.path.join(path_subdir, subexp)

        print("📦 Verificando requisitos adicionais:")
        for linha in verify_lang_resource(path_expapi): print(linha)
        for linha in verify_prisma_schema(path_expapi): print(linha)
        for linha in verify_seed_file(path_expapi): print(linha)
        for linha in verify_user_resource(path_expapi): print(linha)
        for linha in verify_middlewares(path_expapi): print(linha)
        for linha in verify_purchase_resource_extra(path_expapi): print(linha)
        for linha in verify_controller_swagger_summary(path_expapi, 'product'): print(linha)
        for linha in verify_controller_swagger_summary(path_expapi, 'user'): print(linha)
        for linha in verify_swagger_root(path_expapi): print(linha)

if __name__ == "__main__":
    avaliar_todos_os_alunos("./reposTF")
