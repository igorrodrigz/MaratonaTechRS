import requests
from bs4 import BeautifulSoup
import time
import pywhatkit
import openpyxl

#Mapeamento de zonas de impacto
Amarelo = "Pequenos alagamentos possíveis. "
Laranja = "Inundações podem ocorrer."
Vermelho = "Alta probabilidade de inundações na sua área."
Marrom = "Evacuação imediata necessária."
Preto = "ALERTA MÁXIMO"

#Scraping do nível do rio
def obter_nivel_rio(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tag identificadora do nvl do rio
        nivel_rio_tag = soup.find('div', {'id': 'nivel-rio'})
        if nivel_rio_tag:
            nivel_rio = nivel_rio_tag.text.strip()
            try:
                nivel_rio = float(nivel_rio)
            except ValueError:
                print("Não foi possível converter o nível do rio para número.")
                nivel_rio = None
            return nivel_rio
        else:
            print("Não foi possível encontrar o nível do rio na página.")
            return "None"
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter nível do rio: {e}")
        return "None"


# Função para construir a mensagem de alerta
def construir_mensagem(nivel_rio):
    if nivel_rio > 8.5 < 10:
        nivel_alerta = "Amarelo"
        return f"Atenção, risco baixo de enchente. Nível do rio: {nivel_rio}m \nNível de alerta: {nivel_alerta}. {Amarelo}\nMantenha-se informado e evite áreas vulneráveis. Para mais informações : {url_nivel_rio}."
    elif nivel_rio > 10 < 12:
        nivel_alerta = "Laranja"
        return f"Atenção, aviso de risco moderado de enchente. Nível do rio: {nivel_rio}m \nNível de alerta: {nivel_alerta}. {Laranja}\nFique atendo aos boletins metereológicos e evite áreas baixas. "
    elif nivel_rio > 12 < 14:
        nivel_alerta = "Vermelho"
        return f"Atenção, alerta de enchente! Nível do rio: {nivel_rio}m \nNível de alerta: {nivel_alerta}. {Vermelho}\nFique atento aos avisos e prepare-se para possível evacuação."
    elif nivel_rio > 14 > 16:
        nivel_alerta = "Marrom"

        return f"URGENTE! Enchente severa na região. Nível do rio: {nivel_rio}m  \nNível de alerta: {nivel_alerta}. {Marrom}\nProcure abrigo seguro e siga orientações das autoridades."
    elif nivel_rio < 16:
        nivel_alerta = "Preto"
        return f"Alerta máximo, alerta máximo. Nível do rio: {nivel_rio}m \nNivel de alerta: {nivel_alerta}. {Marrom}\nProcure abrigo, siga orientações."
    return "Nível do rio não atingiu o nível de alerta."

# Função para enviar mensagens
def enviar_mensagem(numero_contato, mensagem):
    try:
        pywhatkit.sendwhatmsg_instantly(numero_contato, mensagem, 30, tab_close=False)
        print(f"Mensagem enviada para {numero_contato}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {numero_contato}: {e}")


# Carregar a planilha com os contatos
try:
    lista_contatos_dc = openpyxl.load_workbook('ContatosCidades.xlsx')
    planilha = lista_contatos_dc['Plan1']
except Exception as e:
    print(f"Erro ao carregar a planilha: {e}")
    exit()

# URL do site que fornece o nível do rio
url_nivel_rio = "http://127.0.0.1:5500/AlertaRioUruguai/index.html"
nivel_rio = obter_nivel_rio(url_nivel_rio)

# Iterar sobre as linhas da planilha e enviar mensagens
for linha in planilha.iter_rows(min_row=2, min_col=1, values_only=True):
    numero_contato = linha[0]  # Primeira coluna, índice 0

    # Verificar se o número de telefone não é nulo e está no formato correto
    if numero_contato and isinstance(numero_contato, str) and numero_contato.startswith('+'):
        mensagem = construir_mensagem(nivel_rio)
        enviar_mensagem(numero_contato, mensagem)
        time.sleep(15)  # Aguardar um intervalo entre as mensagens
    else:
        print("Número de telefone inválido ou vazio.")

