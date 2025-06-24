import os
import requests
from time import sleep
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SUBDOMAIN = os.getenv("SUBDOMAIN")
BASE_URL = f"https://{SUBDOMAIN}.kommo.com"

def get_lost_leads():
    url = f"{BASE_URL}/api/v4/leads?filter[statuses][0][status]=lost"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
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
    while True:
        try:
            get_lost_leads()
            sleep(300)  # espera 5 minutos
        except Exception as e:
            print("Erro:", e)
            sleep(60)
