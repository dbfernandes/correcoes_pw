
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
            if 'resource' in root.lower() and substring.lower() == d.lower():
                return os.path.join(root, d)    
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
    nota = 10
    lang_resource = find_resource_directory_with_substring(base_dir, 'lang')
    if not lang_resource:
        nota -= 5
        results.append("Diretório do resource language não encontrado.")
    else:
        controller_file = find_file_by_keyword(lang_resource, 'controller')
        if controller_file:
            content = read_file_content(controller_file)
            if 'res.cookie' in content:
                # res.cookie encontrado no controller do resource language
                results.append("[OK] Controlador do resource language OK.")
            else:
                # res.cookie não encontrado no controller do resource language
                nota -= 5
                results.append("Controlador do resource language não possui função para mudar a linguagem.")
        else:
            # Arquivo controller não encontrado no resource lang
            nota -= 5
            results.append("O controlador do resource language não foi encontrado.")

    middleware_dir = find_middleware_directory(base_dir)
    if middleware_dir:
        found_cookie = False
        for fname in os.listdir(middleware_dir):
            print(fname)
            content = read_file_content(os.path.join(middleware_dir, fname))
            if 'req.cookies' in content and 'res.cookie' in content:
                found_cookie = True
                break
        if found_cookie:
            results.append("[OK] Middleware que cria o cookie lang OK.")
        else:
            nota -= 5
            # Middleware não usa req.cookies e res.cookie
            results.append("Middleware que cria o cookie lang não foi encontrado.")
    else:
        nota -= 5
        results.append("Diretório middleware não encontrado.")
    results.append(f"Nota: {nota}")
    return results

def verify_user_resource(base_dir):
    nota = 10
    results = []
    #### Verifica os modelos em prisma/schema.prisma
    schema_path = os.path.join(base_dir, 'prisma', 'schema.prisma')
    if not os.path.isfile(schema_path):
        nota -= 5
        results.append("Arquivo prisma/schema.prisma não encontrado.")
    else:
        content = read_file_content(schema_path)
        expected_models = ['user', 'type']
        for model in expected_models:
            model_translate = 'essa_string_nao_sera_encontrada'
            if model.lower() == 'user':
                model_translate = 'usuario'
            elif model.lower() == 'type':
                model_translate = 'tipo'                     
            if model.lower() in content or model_translate in content:              
                results.append(f"[OK] Modelo '{model}' encontrado em schema.prisma.")
            else:
                if model.lower() == 'user':
                    nota -= 5
                if model.lower() == 'type':
                    nota -= 2                     
                results.append(f"Modelo '{model}' não encontrado em schema.prisma.")
            
    #### Verifica as seeds
    prisma_dir = os.path.join(base_dir, 'prisma')
    if not os.path.isdir(prisma_dir):
        nota -= 5
        results.append("Diretório prisma não encontrado.")
    else:
        arquivo_seed_encontrado = False
        for fname in os.listdir(prisma_dir):
            if 'seed' in fname.lower() or 'semente' in fname.lower():
                arquivo_seed_encontrado = True
                content = read_file_content(os.path.join(prisma_dir, fname))
                if 'createmany' in content and 'disconnect' in content:
                    # Arquivo de seed encontrado com prisma.createMany e prisma.disconnect.
                    results.append("[OK] Arquivo de seed OK.")
                else:
                    # Arquivo de seed encontrado, mas faltam prisma.createMany ou prisma.disconnect.
                    nota -= 2
                    results.append("Arquivo de seed encontrado, mas está incompleto.")
        if not arquivo_seed_encontrado:
            nota -= 2
            results.append("Arquivo prisma/seed.ts não encontrado.")
      
    #### Verifica o resource      
    user_resource = find_resource_directory_with_substring(base_dir, 'user') or find_resource_directory_with_substring(base_dir, 'usuario')
    if not user_resource:
        # Resource 'user' ou 'usuario' não encontrado
        nota -= 5
        results.append("Resource User não encontrado.")
    else:

        type_file = find_file_by_keyword(user_resource, 'type') or find_file_by_keyword(user_resource, 'tipo')
        if type_file:
            content = read_file_content(type_file)
            if 'create' not in content.lower():
                nota -= 2.0
                results.append("Arquivo de types do resource user não possui um tipo para criação dos usuários.")
            if 'update' not in content.lower():
                nota -= 2.0
                results.append("Arquivo de types do resource user não possui um tipo para atualização dos usuários.")
        else:
            nota -= 2.0
            results.append("Arquivo de types do resource user não encontrado.")

        service_file = find_file_by_keyword(user_resource, 'service') or find_file_by_keyword(user_resource, 'servico')
        if service_file:
            content = read_file_content(service_file)
            extra_keywords = ['bcryptjs', 'gensalt', 'compare', 'create', 'find', 'update', 'delete']
            for kw in extra_keywords:
                if kw not in content:
                    nota -= 1
                    results.append(f"A string '{kw}' não foi encontrado no service.")
        else:
            nota -= 2.0
            results.append("Arquivo de service do resource user não foi encontrado.")
    
        padrao_func = re.compile(
                r"""
                (?P<tipo>
                    (?:async\s+)?function\s+(?P<nome1>\w+) |
                    const\s+(?P<nome2>\w+)\s*=\s*(?:async\s*)?(?:function\s*)?\([^)]*\)\s*=>?
                )
                \s*\{
                """,
                re.VERBOSE
            )
        
        vazias = []
        controller_file = find_file_by_keyword(user_resource, 'controller') or find_file_by_keyword(user_resource, 'controlador')
        if controller_file:
            codigo = read_file_content(controller_file)        
            for match in padrao_func.finditer(codigo):
                nome = match.group("nome1") or match.group("nome2")
                inicio = match.end()  # posição logo após a primeira {
                contador = 1
                i = inicio
                while i < len(codigo) and contador > 0:
                    if codigo[i] == "{":
                        contador += 1
                    elif codigo[i] == "}":
                        contador -= 1
                    i += 1
                corpo = codigo[inicio:i - 1].strip()
                if len(corpo) < 20:
                    vazias.append(nome)      
        
        for vazia in vazias:
            nota -= 1
            results.append(f"A função '{vazia}' não foi implementada no controlador.")        
        
    results.append(f"Nota: {nota}")
    return results            


def verify_middlewares(base_dir):
    nota = 10
    results = []
    middleware_dir = find_middleware_directory(base_dir)
    if not middleware_dir:
        results.append("Diretório middlewares não encontrado.")
        nota = 0
    else:
        for name in ['isAdmin.ts', 'isAuth.ts']:
            path = os.path.join(middleware_dir, name)
            if os.path.isfile(path):
                content = read_file_content(path)
                if 'req.session' in content and 'next' in content:
                    results.append(f"[OK] {name} implementado corretamente.")
                else:
                    results.append(f"{name} não implementado corretamente.")
                    nota -= 3.0
            else:
                results.append(f"Arquivo {name} não encontrado.")
                nota -= 5.0
    results.append(f"Nota: {nota}")
    return results



def verify_purchase_resource_extra(base_dir):
    nota = 10
    results = []
    purchase_resource = find_resource_directory_with_substring(base_dir, 'purchase') or find_resource_directory_with_substring(base_dir, 'compra') or find_resource_directory_with_substring(base_dir, 'order')
    if not purchase_resource:
        nota = 0
        results.append("Resource 'purchase' ou 'compra' não encontrado.")
    else:
        controller = find_file_by_keyword(purchase_resource, 'controller')
        service = find_file_by_keyword(purchase_resource, 'service')
        router = find_file_by_keyword(purchase_resource, 'router')
        schema = find_file_by_keyword(purchase_resource, 'schema')
        types = find_file_by_keyword(purchase_resource, 'type')

        if service:
            content = read_file_content(service)
            if 'prisma' in content and 'create' in content:
                pass
            else:
                nota -= 3
                results.append("Service não possui função para salvar a compra no banco.")

        if controller and service:
            total_lines = count_lines(controller) + count_lines(service)
            if total_lines >= 150:
                results.append(f"[OK] Controller + Service tem {total_lines} linhas (>= 150).")
            else:
                results.append(f"Controller + Service tem {total_lines} linhas (< 150).")
        else:
            if not controller:
                nota -= 3
                results.append("Controller não encontrado.")
            if not controller:
                nota -= 3
                results.append("Service não encontrado.")                

        if router:
            content = read_file_content(router)
            if all(method in content for method in ['get', 'post', 'put', 'delete']):
                results.append("[OK] Router possui todos os métodos (GET, POST, PUT, DELETE).")
            else:
                if ('get' not in content):
                    results.append("Método GET não encontrado no router.")
                if ('post' not in content):
                    results.append("Método POST não encontrado no router.")
                if ('put' not in content):
                    results.append("Método PUT não encontrado no router.")   
                if ('delete' not in content):
                    results.append("Método DELETE não encontrado no router.")                                       
        else:
            results.append("Arquivo router não encontrado.")

        if schema:
            content = read_file_content(schema)
            if 'joi.object' in content:
                results.append("[OK] Schema possui Joi.object.")
            else:
                nota -= 1
                results.append("O Schema Joi não foi implementado corretamente.")
        else:
            nota -= 2
            results.append("Arquivo schema não encontrado.")

        if types:
            lines = count_lines(types)
            if lines > 15:
                results.append(f"[OK] Arquivo Type possui {lines} linhas (> 15).")
            else:
                results.append(f"Arquivo Type possui apenas {lines} linhas (<= 15).")
        else:
            nota -= 2
            results.append("Arquivo type não encontrado.")
    results.append(f"Nota: {nota} (essa nota precisa ser avaliada)")
    return results

def verify_controller_swagger_summary(base_dir):
    results = []
    for resource_name in ['user','product']:
        resource = find_resource_directory_with_substring(base_dir, resource_name)
        if not resource:
            return [f"Resource '{resource_name}' não encontrado."]
        controller = find_file_by_keyword(resource, 'controller')
        if not controller:
            return [f"Controller do resource '{resource_name}' não encontrado."]
        content = read_file_content(controller)
        func_names = re.findall(r'const\s+(\w+)\s*(?::[^=]+)?=\s*async\s*\(', content)
        for name in func_names:
            if f'{name}' in content and 'swagger.summary' in content:
                results.append(f"[OK] Função {name} possui swagger.summary.")
            else:
                results.append(f"Função {name} não possui swagger.summary.")

        swagger_file = os.path.join(base_dir, 'src', 'swagger.ts')
        if os.path.isfile(swagger_file):
            results.append("[OK] Arquivo swagger.ts encontrado na raiz.")
        else:
            results.append("Arquivo swagger.ts não encontrado na raiz.")

        router_dir = os.path.join(base_dir, 'src', 'router')
        count = 0
        if os.path.isdir(router_dir):
            for fname in os.listdir(router_dir):
                path = os.path.join(router_dir, fname)
                content = read_file_content(path)
                count += content.count('swagger.tags')
            results.append(f"[OK] swagger.tags aparece {count} vez(es) em arquivos de /router.")
        else:
            results.append("Diretório /router não encontrado.")
    return results





def avaliar_todos_os_alunos(diretorio_turma):
    for aluno in sorted(os.listdir(diretorio_turma)):
        path_aluno = os.path.join(diretorio_turma, aluno)
        if not os.path.isdir(path_aluno):
            continue

        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print(f"🧑 Avaliando: {aluno}")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

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

        current_dir = os.path.abspath(os.getcwd())
        path_expapi = os.path.join(path_subdir, subexp)
        print (f"code {current_dir}/{path_expapi}")
        print()

        print("Exercício 1: Resource Language")
        for linha in verify_lang_resource(path_expapi): print(linha)
        print()
        print("Exercício 2: Resource User")
        for linha in verify_user_resource(path_expapi): print(linha)
        print()
        print("Exercício 3: Middlewares isAuth e isAdmin")
        for linha in verify_middlewares(path_expapi): print(linha)
        print()
        print("Exercício 4: Resource de compra ou Purchase")
        for linha in verify_purchase_resource_extra(path_expapi): print(linha)
        print()
        print("Exercício 5: Swagger")
        for linha in verify_controller_swagger_summary(path_expapi): print(linha)
        print()

if __name__ == "__main__":
    avaliar_todos_os_alunos("./reposTF")
