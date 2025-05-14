# Scraping eSocial - Extração Automatizada de Dados

Este projeto realiza a extração automatizada de dados do portal eSocial, navegando por múltiplas páginas de listagem de remuneração, salvando os dados em um arquivo CSV e controlando o progresso para permitir retomada em caso de falhas.

## Funcionalidades

- **Automação de Navegação:** Utiliza `pyautogui` para simular interações com o navegador, abrindo páginas, copiando HTML e clicando em botões.
- **Extração de Dados:** Usa `BeautifulSoup` para processar o HTML das páginas e extrair informações como Nome, CPF e status de remuneração.
- **Controle de Progresso:** Salva a última página processada em um arquivo JSON, permitindo retomar a extração do ponto de interrupção.
- **Tolerância a Falhas:** Implementa tentativas automáticas em caso de falha na extração ou navegação, incluindo abertura de novas sessões anônimas.
- **Exportação:** Salva os dados extraídos em um arquivo CSV, com controle para sobrescrever ou anexar conforme o progresso.
- **Finalização Automatizada:** Tenta finalizar a competência no sistema após a extração.

## Requisitos

- Python 3.x
- Bibliotecas: `pyautogui`, `pyperclip`, `beautifulsoup4`, `pandas`

Instale as dependências com:
```bash
pip install pyautogui pyperclip beautifulsoup4 pandas
```

## Como funciona

1. **Início:** O script abre o navegador e acessa o portal do eSocial.
2. **Login:** Simula o login no sistema (ajuste as coordenadas conforme necessário).
3. **Extração:** Para cada página, copia o HTML, extrai os dados da tabela e salva no CSV.
4. **Navegação:** Avança para a próxima página até não encontrar mais o botão "Próxima Página".
5. **Retomada:** Em caso de erro, tenta novamente até o limite definido. Se interrompido, pode ser retomado do ponto de parada.
6. **Finalização:** Após concluir, remove o arquivo de controle de página e tenta finalizar a competência.

## Observações

- O script depende de coordenadas de tela e imagens para automação. Ajuste conforme o seu ambiente.
- O uso de automação pode ser sensível a mudanças na interface do eSocial.
- Recomenda-se rodar o script em ambiente controlado e monitorar a execução.

## Aviso

Este projeto é apenas para fins educacionais e de automação interna. O uso de automação em sistemas de terceiros deve respeitar os termos de uso do serviço.

---
```# Scraping eSocial - Extração Automatizada de Dados

Este projeto realiza a extração automatizada de dados do portal eSocial, navegando por múltiplas páginas de listagem de remuneração, salvando os dados em um arquivo CSV e controlando o progresso para permitir retomada em caso de falhas.

## Funcionalidades

- **Automação de Navegação:** Utiliza `pyautogui` para simular interações com o navegador, abrindo páginas, copiando HTML e clicando em botões.
- **Extração de Dados:** Usa `BeautifulSoup` para processar o HTML das páginas e extrair informações como Nome, CPF e status de remuneração.
- **Controle de Progresso:** Salva a última página processada em um arquivo JSON, permitindo retomar a extração do ponto de interrupção.
- **Tolerância a Falhas:** Implementa tentativas automáticas em caso de falha na extração ou navegação, incluindo abertura de novas sessões anônimas.
- **Exportação:** Salva os dados extraídos em um arquivo CSV, com controle para sobrescrever ou anexar conforme o progresso.
- **Finalização Automatizada:** Tenta finalizar a competência no sistema após a extração.

## Requisitos

- Python 3.x
- Bibliotecas: `pyautogui`, `pyperclip`, `beautifulsoup4`, `pandas`

Instale as dependências com:
```bash
pip install pyautogui pyperclip beautifulsoup4 pandas
```

## Como funciona

1. **Início:** O script abre o navegador e acessa o portal do eSocial.
2. **Login:** Simula o login no sistema (ajuste as coordenadas conforme necessário).
3. **Extração:** Para cada página, copia o HTML, extrai os dados da tabela e salva no CSV.
4. **Navegação:** Avança para a próxima página até não encontrar mais o botão "Próxima Página".
5. **Retomada:** Em caso de erro, tenta novamente até o limite definido. Se interrompido, pode ser retomado do ponto de parada.
6. **Finalização:** Após concluir, remove o arquivo de controle de página e tenta finalizar a competência.

## Observações

- O script depende de coordenadas de tela e imagens para automação. Ajuste conforme o seu ambiente.
- O uso de automação pode ser sensível a mudanças na interface do eSocial.
- Recomenda-se rodar o script em ambiente controlado e monitorar a execução.

## Aviso

Este projeto é apenas para fins educacionais e de automação interna. O uso de automação em sistemas de terceiros deve respeitar os termos de uso do serviço.

---
