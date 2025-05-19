import os
from notion_client import Client
import datetime

notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID") 

notion = Client(auth=notion_token)

def criar_pagina_diaria():
  
    hoje = datetime.date.today()
    data_formatada = hoje.strftime("%Y-%m-%d")  
    dia_da_semana = hoje.weekday()  

    if dia_da_semana in [5, 6]:  # Finais de semana
        propriedades = {
            "@Today": {"title": [{"text": {"content": "@Today"}}]}, 
            "🍲 Fazer marmitas da semana": {"checkbox": False},
            "Data": {"date": {"start": data_formatada}},
        }
    else:  # Dias úteis
        propriedades = {
            "@Today": {"title": [{"text": {"content": "@Today"}}]}, 
            "☕ Café da manhã - 8h": {"checkbox": False},
            "🍽️ Almoço - 13h": {"checkbox": False}, 
            "🏃🏽‍♀️Fazer exercícios - 30min": {"checkbox": False},
            "👩🏾‍🎓Estudo - 20h": {"checkbox": False},
            "Data": {"date": {"start": data_formatada}},
        }

    try:
        nova_pagina = notion.pages.create(
            parent={"database_id": database_id},
            properties=propriedades,
        )
        print(f"🚀 Página criada com sucesso! ID: {nova_pagina['id']}")
    except Exception as e:
        print(f"❌ Erro ao criar a página: {e}")

if __name__ == "__main__":
    criar_pagina_diaria()
