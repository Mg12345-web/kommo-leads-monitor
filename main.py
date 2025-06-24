import os
import requests
from time import sleep
from dotenv import load_dotenv
from sheets import enviar_para_planilha
from datetime import datetime

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SUBDOMAIN = os.getenv("SUBDOMAIN")
BASE_URL = f"https://{SUBDOMAIN}.kommo.com"
SHEET_ID = os.getenv("SHEET_ID")
ABA = "Leads Perdidos"

def calcular_dias(inicio, fim):
    try:
        data1 = datetime.fromtimestamp(inicio)
        data2 = datetime.fromtimestamp(fim)
        return (data2 - data1).days
    except:
        return ""

def get_lost_leads():
    url = f"{BASE_URL}/api/v4/leads?filter[statuses][0][status]=lost"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()["_embedded"]["leads"]
    print(f"🔎 Leads perdidos encontrados: {len(data)}")

    dados_para_planilha = []

    for lead in data:
        nome = lead.get("name", "Sem nome")

        telefone = ""
        telefone = ""
campos = lead.get("custom_fields_values")
if campos and isinstance(campos, list):
    for campo in campos:
        if campo.get("field_name", "").lower() in ["telefone", "phone"]:
            telefone = campo["values"][0]["value"]
            break

        motivo = lead.get("loss_reason", {}).get("name", "Sem motivo")
        dias_ate_perda = calcular_dias(lead.get("created_at"), lead.get("updated_at"))
        tempo_sem_resposta = "não implementado"

        print(f"❌ {nome} | Motivo: {motivo}")
        dados_para_planilha.append([nome, telefone, motivo, dias_ate_perda, tempo_sem_resposta])

    if dados_para_planilha:
        enviar_para_planilha(
            sheet_id=SHEET_ID,
            aba_nome=ABA,
            dados=dados_para_planilha
        )
    else:
        print("⚠️ Nenhum dado para enviar à planilha.")

if __name__ == "__main__":
    while True:
        try:
            get_lost_leads()
            sleep(300)
        except Exception as e:
            print("Erro:", e)
            sleep(60)
