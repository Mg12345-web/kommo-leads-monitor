import os
import requests
from time import sleep
from dotenv import load_dotenv

load_dotenv()

# Variáveis de ambiente
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTH_CODE = os.getenv("AUTHORIZATION_CODE")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SUBDOMAIN = os.getenv("SUBDOMAIN")

BASE_URL = f"https://{SUBDOMAIN}.kommo.com"

# Token armazenado em memória (pode usar refresh depois)
access_token = None

def authenticate():
    global access_token
    url = f"{BASE_URL}/oauth2/access_token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": AUTH_CODE,
        "redirect_uri": REDIRECT_URI
    }
    r = requests.post(url, json=payload)
    r.raise_for_status()
    data = r.json()
    access_token = data["access_token"]
    print("✅ Autenticado com sucesso.")

def get_lost_leads():
    url = f"{BASE_URL}/api/v4/leads?filter[statuses][0][status]=lost"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()["_embedded"]["leads"]
    print(f"🔎 Leads perdidos encontrados: {len(data)}")
    for lead in data:
        name = lead["name"]
        pipeline_id = lead["pipeline_id"]
        status_id = lead["status_id"]
        print(f"❌ {name} | Pipeline: {pipeline_id} | Etapa: {status_id}")

if __name__ == "__main__":
    authenticate()
    while True:
        try:
            get_lost_leads()
            sleep(300)  # Espera 5 minutos
        except Exception as e:
            print("Erro:", e)
            sleep(60)
