import webbrowser
import pyautogui
import time
import pyperclip
from bs4 import BeautifulSoup
import pandas as pd
import json
import os

ARQUIVO_ULTIMA_PAGINA = "ultima_pagina.json"
MAX_RETRY_PAGE = 3

def salvar_ultima_pagina(pagina):
    try:
        with open(ARQUIVO_ULTIMA_PAGINA, 'w') as f:
            json.dump({'ultima_pagina': pagina}, f)
        print(f"💾 Última página salva: {pagina}")
    except Exception as e:
        print(f"❌ Erro ao salvar a última página: {e}")

def carregar_ultima_pagina():
    try:
        with open(ARQUIVO_ULTIMA_PAGINA, 'r') as f:
            data = json.load(f)
            pagina = int(data.get('ultima_pagina', 1))
            return pagina if pagina >= 1 else 1
    except FileNotFoundError:
        return 1
    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️ Erro ao decodificar JSON ou valor inválido no arquivo '{ARQUIVO_ULTIMA_PAGINA}': {e}. Iniciando da página 1.")
        return 1
    except Exception as e:
        print(f"⚠️ Erro inesperado ao carregar a última página: {e}. Iniciando da página 1.")
        return 1

def copiar_html_com_retentativas(max_tentativas=3):
    for tentativa in range(1, max_tentativas + 1):
        try:
            print(f"📋 Tentando copiar HTML (tentativa {tentativa}/{max_tentativas})...")
            pyautogui.hotkey('ctrl', 'u')
            time.sleep(3 + tentativa)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)
            html = pyperclip.paste()
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(2)
            if html and '<html' in html.lower():
                print("✅ HTML copiado com sucesso.")
                return html
            else:
                print(f"❌ Tentativa {tentativa}: Conteúdo copiado não parece HTML válido.")
        except Exception as e:
            print(f"❌ Erro durante a tentativa {tentativa} de copiar HTML: {e}")
            try:
                 pyautogui.hotkey('ctrl', 'w')
                 time.sleep(2)
            except:
                 pass
    print(f"❌ Todas as {max_tentativas} tentativas de copiar HTML falharam.")
    return None

def verificar_elemento(seletor_imagem=None, tipo='button', texto_esperado=None, max_tentativas=5, aguardar=2):
    print(f"🔎 Verificando elemento: Tipo='{tipo}', Imagem='{seletor_imagem}', Texto='{texto_esperado}'...")
    for tentativa in range(1, max_tentativas + 1):
        try:
            if tipo == 'button' and seletor_imagem:
                elemento = pyautogui.locateCenterOnScreen(seletor_imagem, confidence=0.9)
                if elemento:
                    print(f"✅ Tentativa {tentativa}: Botão (imagem) encontrado em {elemento}.")
                    return elemento
            elif tipo == 'text' and texto_esperado:
                html_source = pyperclip.paste()
                if texto_esperado in html_source:
                     print(f"✅ Tentativa {tentativa}: Texto '{texto_esperado}' encontrado no HTML.")
                     return True
            elif tipo == 'titulo' and texto_esperado:
                html_source = pyperclip.paste()
                soup = BeautifulSoup(html_source, 'html.parser')
                titulo_element = soup.find('h2', class_='titulo-tabela')
                if titulo_element and titulo_element.text.strip() == texto_esperado:
                    print(f"✅ Tentativa {tentativa}: Título '{texto_esperado}' encontrado no HTML.")
                    return True
            if tipo != 'button' or not elemento:
                 print(f"⏳ Tentativa {tentativa}: '{tipo}' não encontrado. Aguardando {aguardar}s...")
                 time.sleep(aguardar)
            elif tipo == 'button' and elemento:
                 pass
        except pyautogui.ImageNotFoundException:
             print(f"⏳ Tentativa {tentativa}: Imagem '{seletor_imagem}' não encontrada na tela.")
             time.sleep(aguardar)
        except Exception as e:
            print(f"⏳ Tentativa {tentativa}: Erro ao verificar '{tipo}': {e}. Aguardando {aguardar}s...")
            time.sleep(aguardar)
    print(f"❌ Falha ao encontrar '{tipo}' após {max_tentativas} tentativas.")
    return False

def extrair_tabela(html, pagina):
    soup = BeautifulSoup(html, 'html.parser')
    linhas = soup.find_all('tr')
    dados = []
    print(f"\n--- Dados extraídos da Página {pagina} ---")
    registros_encontrados_pagina = 0
    if not linhas:
         print(f"⚠️ ALERTA: Nenhuma linha '<tr>' encontrada no HTML da página {pagina}. A estrutura da tabela mudou?")
         return []
    for i, linha in enumerate(linhas):
        if linha.find('th'):
            continue
        cpf_tag = linha.find('td', class_='chave left')
        nome_tag = None
        tds_com_classe_left = linha.find_all('td', class_='left')
        for td_candidata in tds_com_classe_left:
             classes_da_td_candidata = td_candidata.get('class', [])
             if 'chave' not in classes_da_td_candidata:
                  nome_tag = td_candidata
                  break
        if cpf_tag and nome_tag:
            cpf = cpf_tag.text.strip()
            nome = nome_tag.text.strip()
            if nome == cpf:
                 is_cpf_like = all(c.isdigit() or c in ['.', '-'] for c in nome.replace('.', '').replace('-', ''))
                 if is_cpf_like and len(nome.replace('.', '').replace('-', '')) >= 11:
                     print(f"⚠️ ALERTA DE EXTRAÇÃO (Linha ~{i+1}, Página {pagina}): Nome ('{nome}') parece ser um CPF. Verifique a estrutura da tabela.")
            possui_remuneracao_tag = linha.find('a', string="Ver Remuneração")
            possui_remuneracao = "Possui remuneração" if possui_remuneracao_tag else "Não possui remuneração"
            print(f"🧾 Nome: {nome}, CPF: {cpf}, Status: {possui_remuneracao}")
            dados.append([nome, cpf, possui_remuneracao])
            registros_encontrados_pagina += 1
    if registros_encontrados_pagina == 0:
        print(f"⚠️ Nenhum registro com CPF e Nome encontrado na página {pagina}. Verifique o HTML e seletores.")
    else:
        print(f"------------------------------------")
    return dados

def finalizar_competencia():
    print("\n🏁 Tentando finalizar a competência...")
    localizacao_botao = verificar_elemento(r'./imagens/botao_finalizar.png', tipo='button', max_tentativas=10, aguardar=3)
    if localizacao_botao:
        try:
            pyautogui.click(localizacao_botao)
            print("✅ Competência finalizada com sucesso (clique simulado).")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Erro ao clicar no botão de finalizar: {e}")
    else:
        print("❌ Falha ao encontrar o botão de finalizar competência após várias tentativas.")

def realizar_login():
    print("\n🔑 Realizando login no eSocial...")
    try:
        pyautogui.click(x=-911, y=315); time.sleep(3)
        pyautogui.click(x=-1085, y=635); time.sleep(3)
        pyautogui.click(x=-1405, y=180); time.sleep(1)
        pyautogui.click(x=-1203, y=405); time.sleep(8)
        print("✅ Login simulado concluído.")
        time.sleep(5)
    except Exception as e:
        print(f"❌ Erro durante a simulação do login: {e}")

inicio_total = time.time()
competencia = "202504"
nome_arquivo = f"folha_completa_{competencia}.csv"
pagina = carregar_ultima_pagina()
print(f"▶️ Iniciando ou retomando da página {pagina} para a competência {competencia}.")
webbrowser.open('about:blank')
time.sleep(2)
webbrowser.open('https://login.esocial.gov.br/login.aspx')
time.sleep(5)
realizar_login()
todos_dados_acumulados = []
total_registros_extraidos = 0
houve_erro_na_ultima_pagina = False
tentativas_pagina_atual = 0

while True:
    print(f"\n--- Processando página {pagina} (Tentativa {tentativas_pagina_atual + 1}/{MAX_RETRY_PAGE+1}) ---")
    tempo_inicio_extracao = time.time()
    if pagina == 1:
        url_pagina_atual = f"https://www.esocial.gov.br/portal/FolhaPagamento/ListaRemuneracao?Competencia={competencia}&Tipo=1200&PossuiDae=False"
    else:
         url_pagina_atual = f"https://www.esocial.gov.br/portal/FolhaPagamento/ListaRemuneracao?Competencia={competencia}&Tipo=1200&Pagina=e{pagina}-o0&EhBeneficiario=False"
         try:
             print(f"↪️ Tentando fechar aba anterior...")
             pyautogui.hotkey('ctrl', 'w')
             time.sleep(2)
         except Exception as e:
              print(f"⚠️ Erro ao tentar fechar aba anterior: {e}")
    print(f"🌐 Abrindo URL: {url_pagina_atual}")
    webbrowser.open(url_pagina_atual)
    time.sleep(10)
    time.sleep(5)
    html_atual = copiar_html_com_retentativas()
    if not html_atual:
        print(f"❌ Falha crítica ao obter HTML da página {pagina}. Iniciando lógica de nova tentativa/desistência.")
        houve_erro_na_ultima_pagina = True
        tentativas_pagina_atual += 1
        if tentativas_pagina_atual > MAX_RETRY_PAGE:
            print(f"❌ Limite de {MAX_RETRY_PAGE+1} tentativas excedido para a página {pagina}. Desistindo da extração.")
            break
        else:
            print(f"🔄 Tentando novamente a página {pagina} em uma nova sessão anônima...")
            try:
                print("↪️ Fechando janela/aba atual...")
                for _ in range(3):
                     pyautogui.hotkey('ctrl', 'w')
                     time.sleep(1)
                time.sleep(3)
            except Exception as e:
                 print(f"⚠️ Erro ao tentar fechar janela/aba: {e}")
            print(" stealth Abrindo nova guia anônima (Ctrl+Shift+N)...")
            pyautogui.hotkey('ctrl', 'shift', 'n')
            time.sleep(5)
            realizar_login()
            continue
    dados_atuais = extrair_tabela(html_atual, pagina)
    if dados_atuais:
        df_atual = pd.DataFrame(dados_atuais, columns=['Nome', 'CPF', 'Status Remuneração'])
        try:
            arquivo_existe = os.path.exists(nome_arquivo)
            modo = 'a'
            header = not arquivo_existe
            if pagina == 1 and not arquivo_existe:
                 header = True
            elif pagina == 1 and arquivo_existe and carregar_ultima_pagina() == 1:
                 modo = 'w'
                 header = True
                 print(f"🔄 Sobrescrevendo arquivo '{nome_arquivo}' para a página 1.")
            df_atual.to_csv(nome_arquivo, index=False, encoding='utf-8-sig', mode=modo, header=header)
            print(f"💾 Página {pagina}: {len(dados_atuais)} registros {'salvos' if modo == 'w' else 'anexados'} a '{nome_arquivo}'.")
            salvar_ultima_pagina(pagina)
            tentativas_pagina_atual = 0
        except Exception as e:
            print(f"❌ Erro ao salvar dados da página {pagina} no arquivo: {e}")
            houve_erro_na_ultima_pagina = True
    else:
         print(f"⚠️ Extração da página {pagina} não retornou dados.")
    soup_atual = BeautifulSoup(html_atual, 'html.parser')
    botao_proxima_html = soup_atual.find('a', id='proxima-pagina', string='Próxima Página ❯')
    if botao_proxima_html:
        print(f"✅ Botão 'Próxima Página' encontrado no HTML da página {pagina}.")
        pagina_anterior = pagina
        pagina += 1
    else:
        print(f"⛔ Botão 'Próxima Página' **não** encontrado no HTML da página {pagina}. Iniciando validações alternativas...")
        localizacao_botao_imagem = verificar_elemento(r'./imagens/botao_proxima_pagina.png', tipo='button', max_tentativas=3, aguardar=2)
        if localizacao_botao_imagem:
            print("✅ Validação 1: Botão 'Próxima Página' encontrado pela imagem após tentativas. Tentando clicar...")
            try:
                pyautogui.click(localizacao_botao_imagem)
                print("✅ Clique simulado no botão 'Próxima Página'.")
                time.sleep(7)
                pagina += 1
                tentativas_pagina_atual = 0
                continue
            except Exception as e:
                print(f"❌ Erro ao clicar no botão 'Próxima Página' pela imagem: {e}. Falha na navegação.")
        elif verificar_elemento(None, tipo='text', texto_esperado='Trabalhadores sem Vínculo de Emprego'):
            print("✅ Validação 2: Texto 'Trabalhadores sem Vínculo de Emprego' encontrado. Fim da navegação principal (provavelmente última página da lista 1200).")
            break
        elif verificar_elemento(None, tipo='titulo', texto_esperado='Trabalhadores sem Vínculo de Emprego'):
            print("✅ Validação 3: Título da tabela 'Trabalhadores sem Vínculo de Emprego' encontrado. Fim da navegação principal (provavelmente última página da lista 1200).")
            break
        else:
            print(f"❌ Todas as validações falharam na página {pagina}. Iniciando lógica de nova tentativa/desistência.")
            houve_erro_na_ultima_pagina = True
            tentativas_pagina_atual += 1
            if tentativas_pagina_atual > MAX_RETRY_PAGE:
                print(f"❌ Limite de {MAX_RETRY_PAGE+1} tentativas excedido para a página {pagina}. Desistindo da extração.")
                break
            else:
                print(f"🔄 Tentando novamente a página {pagina} em uma nova sessão anônima (Tentativa {tentativas_pagina_atual}/{MAX_RETRY_PAGE})...")
                try:
                    print("↪️ Fechando janela/aba atual...")
                    for _ in range(3):
                         pyautogui.hotkey('ctrl', 'w')
                         time.sleep(1)
                    time.sleep(3)
                except Exception as e:
                     print(f"⚠️ Erro ao tentar fechar janela/aba: {e}")
                print(" stealth Abrindo nova guia anônima (Ctrl+Shift+N)...")
                try:
                    pyautogui.hotkey('ctrl', 'shift', 'n')
                    time.sleep(5)
                except Exception as e:
                     print(f"❌ Erro ao tentar abrir guia anônima: {e}")
                     time.sleep(5)
                realizar_login()
                continue
    tempo_fim_extracao = time.time()
    print(f"⏱️ Tempo para processar página {pagina - 1}: {(tempo_fim_extracao - tempo_inicio_extracao):.2f} seg.")
    print(f"⏱️ Tempo total acumulado: {(tempo_fim_extracao - inicio_total):.2f} seg.")

print("\n--- Extração Concluída ---")
try:
    if os.path.exists(nome_arquivo):
        df_final = pd.read_csv(nome_arquivo, encoding='utf-8-sig')
        total_registros_extraidos = len(df_final)
        print(f"📊 Total de registros extraídos no arquivo '{nome_arquivo}': {total_registros_extraidos}.")
    else:
        total_registros_extraidos = 0
        print(f"⚠️ Arquivo '{nome_arquivo}' não encontrado ao final.")
except Exception as e:
    print(f"❌ Erro ao ler o arquivo CSV final: {e}")
    total_registros_extraidos = "Desconhecido devido a erro"
finalizar_competencia()
if not houve_erro_na_ultima_pagina and total_registros_extraidos > 0:
   try:
       if os.path.exists(ARQUIVO_ULTIMA_PAGINA):
           os.remove(ARQUIVO_ULTIMA_PAGINA)
           print("🧹 Arquivo de última página removido (extração concluída com sucesso).")
       else:
           print("ℹ️ Arquivo de última página não encontrado para remover.")
   except Exception as e:
       print(f"⚠️ Erro ao remover o arquivo de última página: {e}")
elif houve_erro_na_ultima_pagina:
     print(f"⚠️ Arquivo de última página '{ARQUIVO_ULTIMA_PAGINA}' mantido devido a erro durante a extração.")
else:
     print("ℹ️ Arquivo de última página mantido (nenhum dado extraído).")
fim_total = time.time()
print(f"\n⏱️ Tempo total de execução: {(fim_total - inicio_total):.2f} seg.")