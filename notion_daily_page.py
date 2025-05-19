import os
from notion_client import Client
import datetime

notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")

notion = Client(auth=notion_token)

def criar_pagina_diaria():
    hoje = datetime.date.today()
    nome_pagina = "@Today"
    dia_da_semana = hoje.weekday()

    if dia_da_semana in [5, 6]: 
        propriedades = {
            "🍲 Fazer marmitas da semana": {"checkbox": False},
        }
    else: 
        propriedades = {
            "☕ Café da manhã - 8h": {"checkbox": False},
            "🍽️ Almoço - 13h": {"checkbox": False},
            "🏃🏽‍♀️Fazer exercicios - 30min": {"checkbox": False},
            "👩🏾‍🎓Estudo - 20h": {"checkbox": False},
        }

    notion.pages.create(
        parent={"database_id": database_id},
        properties=propriedades
    )
    print(f"Página '{nome_pagina}' criada com sucesso!")

if __name__ == "__main__":
    criar_pagina_diaria()
