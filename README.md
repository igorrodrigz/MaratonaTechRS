# Maratona Virtual de Ajuda ao Rio Grande do Sul - Sistema de Alerta para a Defesa Civil

Este projeto faz parte da Maratona Virtual de Ajuda ao Estado do Rio Grande do Sul. O objetivo desta aplicação é monitorar o nível do rio e enviar alertas para a Defesa Civil em caso de riscos de inundações. O sistema utiliza scraping para obter o nível do rio de uma página web, constrói mensagens de alerta com base no nível obtido e envia essas mensagens para os contatos registrados.

## Funcionalidades

- **Monitoramento do Nível do Rio**: Scraping do nível do rio a partir de uma URL fornecida.
- **Construção de Mensagens de Alerta**: Mensagens personalizadas com base no nível do rio.
- **Envio de Alertas via WhatsApp**: Envio automático de mensagens de alerta para contatos registrados em uma planilha Excel.

## Estrutura do Código

### Mapeamento de Zonas de Impacto

```python
Amarelo = "Pequenos alagamentos possíveis."
Laranja = "Inundações podem ocorrer."
Vermelho = "Alta probabilidade de inundações na sua área."
Marrom = "Evacuação imediata necessária."
Preto = "ALERTA MÁXIMO"
```

### Funções Principais

#### 1. `obter_nivel_rio(url)`

Obtém o nível do rio a partir de uma página web especificada pela URL.

```python
def obter_nivel_rio(url):
        nivel_rio_tag = soup.find('input', {'id': 'valor_medicao'})
        if nivel_rio_tag and 'value' in nivel_rio_tag.attrs:
            nivel_rio_text = nivel_rio_tag['value'].strip()
            nivel_rio = nivel_rio_text.replace(',', '.').strip()
```

#### 2. `construir_mensagem(nivel_rio)`

Constrói uma mensagem de alerta com base no nível do rio.

```python
def construir_mensagem(nivel_rio):
        if 8.5 < nivel_rio <= 10:
        nivel_alerta = "Amarelo"
        return f"Atenção, risco baixo de enchente. Nível do rio: {nivel_rio}m\nNível de alerta: {nivel_alerta}. Nessa cota as áreas atingidas são ribeirinhas e vegetação. {Amarelo}\nMantenha-se informado e evite áreas vulneráveis. Para mais informações: {url_nivel_rio}."
    elif 10 < nivel_rio <= 12:
        nivel_alerta = "Laranja"
        return f"Atenção, aviso de risco moderado de enchente. Nível do rio: {nivel_rio}m\nNível de alerta: {nivel_alerta}. Bairros atingidos parcialmente: Mascarenhas de Morais, Bela Vista, Francisca Tarrago, Cabo Luiz Quevedo, Alexandre Zachia, Santana, Santo Antônio; e minimamente: Rio Branco, Cidade Nova e Jóquei Clube. {Laranja}\nFique atento aos boletins meteorológicos e evite áreas baixas. Para mais informações: {url_nivel_rio}."
    elif 12 < nivel_rio <= 13:
        nivel_alerta = "Vermelho"
        return f"Atenção, alerta de enchente! Nível do rio: {nivel_rio}m\nNível de alerta: {nivel_alerta}. Bairros atingidos totalmente: Mascarenhas de Morais; e minimamente: Bela Vista, Francisca Tarrago, Cabo Luiz Quevedo, Alexandre Zachia, Santana, Santo Antônio e Jóquei Clube. {Vermelho}\nFique atento aos avisos e prepare-se para possível evacuação. Para mais informações: {url_nivel_rio}."
    elif 13 < nivel_rio <= 14:
        nivel_alerta = "Marrom"
        return f"URGENTE! Enchente severa na região. Nível do rio: {nivel_rio}m\nNível de alerta: {nivel_alerta}. Bairros atingidos totalmente: Mascarenhas de Morais; e parcialmente: Bela Vista, Francisca Tarrago, Cabo Luiz Quevedo, Alexandre Zachia, Santana, Santo Antônio e Jóquei Clube. {Marrom}\nProcure abrigo seguro e siga orientações das autoridades. Para mais informações: {url_nivel_rio}."
    elif nivel_rio > 14:
        nivel_alerta = "Preto"
        return f"Alerta máximo, alerta máximo. Nível do rio: {nivel_rio}m\nNível de alerta: {nivel_alerta}. Bairros atingidos totalmente: Mascarenhas de Morais e Francisca Tarrago; e parcialmente: Bela Vista, Cabo Luiz Quevedo, Alexandre Zachia, Santana, Santo Antônio e Jóquei Clube. {Preto}\nProcure abrigo, siga orientações. Para mais informações: {url_nivel_rio}."
    return "Nível do rio não atingiu o nível de alerta."
```

#### 3. `enviar_mensagem(numero_contato, mensagem)`

Envia uma mensagem de alerta para um número de contato via WhatsApp.

```python
def enviar_mensagem(numero_contato, mensagem):
     pywhatkit.sendwhatmsg_instantly(numero_contato, mensagem, 30, tab_close=True)
        print(f"Mensagem enviada para {numero_contato}")
```

### Carregamento da Planilha de Contatos

Carrega uma planilha Excel com os contatos para os quais os alertas serão enviados.

```python
try:
    lista_contatos_dc = openpyxl.load_workbook('ContatosCidades.xlsx')
    planilha = lista_contatos_dc['Plan1']
except Exception as e:
    print(f"Erro ao carregar a planilha: {e}")
    exit()
```

### Execução do Sistema

Obtém o nível do rio e envia alertas para os contatos registrados.

```python
url_nivel_rio = "http://127.0.0.1:5500/AlertaRioUruguai/index.html"
nivel_rio = obter_nivel_rio(url_nivel_rio)

if nivel_rio is not None:
    for linha in planilha.iter_rows(min_row=2, min_col=1, values_only=True):
        numero_contato = linha[0]  # Primeira coluna, índice 0

        if numero_contato and isinstance(numero_contato, str) and numero_contato.startswith('+'):
            mensagem = construir_mensagem(nivel_rio)
            enviar_mensagem(numero_contato, mensagem)
            time.sleep(15) 
```

## Requisitos

- Python 3.x
- Bibliotecas: `requests`, `beautifulsoup4`, `pywhatkit`, `openpyxl`

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/igorrodrigz/MaratonaTechRS.git
   ```

2. Instale as dependências:
   ```bash
   pip install requests beautifulsoup4 pywhatkit openpyxl
   ```

3. Configure a URL do nível do rio e a planilha de contatos.

## Uso

1. Execute o script:
   ```bash
   python app.py
   ```

## Contribuição

Sinta-se à vontade para abrir issues e pull requests. Para maiores informações, consulte o repositório no GitHub.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais informações.

---

**Contato do Desenvolvedor:**
https://www.linkedin.com/in/igorrodriguesdevpy/

Igor Rodrigues  
[Repositório no GitHub](https://github.com/igorrodrigz/MaratonaTechRS)
