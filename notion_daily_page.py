import os
from notion_client import Client
import datetime

notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")
notion = Client(auth=notion_token)

def criar_pagina_diaria():
    hoje = datetime.date.today() 
    data_formatada = hoje.strftime("%Y-%m-%d")   
    data_formatada = hoje.strftime("%d-%m-%Y")
    dia_da_semana = hoje.weekday()
    

    if dia_da_semana in [5, 6]:  # Finais de semana (sábado e domingo)
        propriedades = {
            "🍲 Fazer marmitas da semana": {"checkbox": False}, 
            "Data": {"date": {"start": data_formatada}},
        }
        print("✨ Criando página com a propriedade '🍲 Fazer marmitas da semana' para o final de semana.")
    else:  # Dias úteis (segunda a sexta)
        propriedades = {
            "☕ Café da manhã - 8h": {"checkbox": False},
            "🍽️ Almoço - 13h": {"checkbox": False},
            "🏃🏽‍♀️Fazer exercícios - 30min": {"checkbox": False},
            "👩🏾‍🎓Estudo - 20h": {"checkbox": False},
            "Data": {"date": {"start": data_formatada}}, 
        }
        print("✨ Criando página com propriedades para dia útil.")

    try:
        nova_pagina = notion.pages.create(
            parent={"database_id": database_id},
            properties={
                **propriedades,
                "Name": {"title": [{"text": {"content": data_formatada}}]}
            }
        )
        print(f"🚀 Página '{titulo_pagina}' criada com sucesso! ID: {nova_pagina['id']}")
    except Exception as e:
        print(f"❌ Erro ao criar a página: {e}")

if __name__ == "__main__":
    criar_pagina_diaria()
