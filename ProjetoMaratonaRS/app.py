import requests
from bs4 import BeautifulSoup
import time
import pywhatkit
import openpyxl

# Mapeamento das zonas de impacto (cores)
ALERTAS = {
    "Amarelo": "Pequenos alagamentos possíveis,",
    "Laranja": "Inundações podem ocorrer.",
    "Vermelho": "Alta probabilidade de inundações na sua área.",
    "Marrom": "Evacuação imediata necessária.",
    "Preto": "ALERTA MAXIMO"
}

# Scraping do nível do rio
def obter_nivel_rio(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Verificação se a requisição foi bem-sucedida
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tag identificadora do nível do rio pelo id valor_medicao
        nivel_rio_tag = soup.find('input', {'id': 'valor_medicao'})
        if nivel_rio_tag and 'value' in nivel_rio_tag.attrs:
            nivel_rio_text = nivel_rio_tag['value'].strip()
            nivel_rio = nivel_rio_text.replace(',','.').strip()
            try:
                return float(nivel_rio)
            except ValueError:
                print("Não foi possível converter o nível do rio para número.")
                return None
        else:
            print("Não foi possível encontrar o nível do rio na página.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter nível do rio: {e}")
        return None

# Função para construir a mensagem de alerta
def construir_mensagem(nivel_rio, url):
    if nivel_rio is None:
        return "Erro ao obter o nível do rio, não foi possível gerar a mensagem de alerta"

    if 8.5 < nivel_rio <= 10:
        nivel_alerta = "Amarelo"
    elif 10 < nivel_rio <= 12:
        nivel_alerta = "Laranja"
    elif 12 < nivel_rio <= 13:
        nivel_alerta = "Vermelho"
    elif 13 < nivel_rio <= 14:
        nivel_alerta = "Marrom"
    elif nivel_rio > 14:
        nivel_alerta = "Preto"
    else:
        return "Nível do rio não atingiu o nível de alerta."

    return (
        f"Atenção, risco de enchente. Nível do rio: {nivel_rio}m\n"
        f"Nível de alerta: {nivel_alerta}, {ALERTAS[nivel_alerta]}\n"
        f"Mantenha-se informado e evite áreas vulneráveis. Para mais informações: {url}."
    )

#Função para enviar mensagens
def enviar_mensagem(numero_contato, mensagem):
    try:
        pywhatkit.sendwhatmsg_instantly(numero_contato, mensagem, 30, tab_close=True)
        print(f"Mensagem enviada para {numero_contato}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {numero_contato}: {e}")

# Carregar a planilha com os contatos
try:
    lista_contatos_dc = openpyxl.load_workbook('../ContatosCidades.xlsx')
    planilha = lista_contatos_dc['plan1']
except Exception as e:
    print(f"erro ao carregar a planilha: {e}")
    exit()

# URL do site que fornece o nível do rio (alerta.ai)
url_nivel_rio = "http://baseconsultoria.com.br/alertaai/?medida=11.5"
nivel_rio = obter_nivel_rio(url_nivel_rio)

# Verificar se o nível do rio foi obtido
if nivel_rio is not None:
    #iterar sobre as linhas da planilha para enviar mensagens
    for linha in planilha.iter_rows(min_row=2, min_col=1, values_only=True):
        numero_contato = linha[0] # primeira coluna, indice 0 (cabeçalho)

        #Verificar se o número de telefone não é nulo e está no formato correto
        if numero_contato and isinstance(numero_contato, str) and numero_contato.startswith('+'):
            mensagem = construir_mensagem(nivel_rio, url_nivel_rio)
            enviar_mensagem(numero_contato, mensagem)
            time.sleep(15)#Aguardar intervalo de carregamento da janela
        else:
            print("Número de telefone inválido ou vazio")
else:
    print("Erro ao obter o nível do rio, não foi possível enviar mensagens de alerta.")