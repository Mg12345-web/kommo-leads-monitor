import os
import json
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

def carregar_credenciais():
    # Lê e reconstrói o JSON das credenciais
    json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not json_str:
        raise Exception("Variável GOOGLE_CREDENTIALS_JSON não encontrada")

    # Remove barras invertidas extras (\n -> quebra real de linha)
    json_str = json_str.encode().decode("unicode_escape")
    info = json.loads(json_str)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    return Credentials.from_service_account_info(info, scopes=scopes)

def enviar_para_planilha(sheet_id, aba_nome, dados):
    creds = carregar_credenciais()
    client = gspread.authorize(creds)
    
    try:
        sheet = client.open_by_key(sheet_id).worksheet(aba_nome)
    except gspread.exceptions.WorksheetNotFound:
        # Cria a aba se não existir
        sheet = client.open_by_key(sheet_id).add_worksheet(title=aba_nome, rows="1000", cols="10")

    # Cabeçalho fixo
    cabecalho = ["Nome", "Telefone", "Motivo da perda", "Dias até a perda", "Tempo sem resposta"]
    sheet.clear()
    sheet.append_row(cabecalho)
    for linha in dados:
        sheet.append_row(linha)
