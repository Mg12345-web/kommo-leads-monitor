import os
import json
import gspread
from google.oauth2.service_account import Credentials

def conectar_sheets():
    # Recupera a variável com as credenciais JSON escapadas
    json_credenciais = os.getenv("GOOGLE_CREDENTIALS_JSON")

    # Carrega o JSON como dicionário
    info = json.loads(json_credenciais)

    # Cria as credenciais
    credenciais = Credentials.from_service_account_info(info, scopes=[
        "https://www.googleapis.com/auth/spreadsheets"
    ])

    # Autentica no Google Sheets
    client = gspread.authorize(credenciais)
    return client

def enviar_para_planilha(sheet_id, aba_nome, dados):
    client = conectar_sheets()
    planilha = client.open_by_key(sheet_id)
    aba = planilha.worksheet(aba_nome)

    # Envia os dados (sobrescreve a aba)
    aba.clear()
    aba.append_row(["Nome da Vendedora", "Telefone do Cliente", "Motivo", "Dias até perda", "Tempo sem resposta"])
    
    for item in dados:
        aba.append_row(item)
