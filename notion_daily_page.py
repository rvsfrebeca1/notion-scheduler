
import os
from notion_client import Client
import datetime

# --- CONFIGURAÇÕES ---
notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")

notion = Client(auth=notion_token)

LEMBRETES_MENSAIS = {
    30: [
            {
                "mensagem": "Hoje é dia de checklist financeiro mensal!",
                "url": "https://www.notion.so/H-BITO-Juntar-dinheiro-mensalmente-2cc6877ef64580df94cfe074814f71b3",
                "emoji": "💰"
            },
            {
                "mensagem": "E, ai. Vamos revisar as metas de 2026 e ver o que ainda faz sentido ou não? Seja sincera consigo mesma!",
                "url": "https://www.notion.so/Planos-pessoais-por-prioridade-7ee8cb657df94cbea68deb61767d904c",
                "emoji": "⚠️"
            }
    ]
}

# 2. Regra Semanal
AVISO_SEXTA_FEIRA = {
    "mensagem": "Sextou! Preencha o relatório semanal e lembre-se de curtir o final de semana com responsabilidade",
    "url": "https://www.notion.so/H-BITOS-Rotina-saud-vel-2cc6877ef6458050a7d4f1f955a08671",
    "emoji": "🍺"
}

def criar_bloco_aviso(texto, url, emoji="🔔"):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "icon": {"emoji": emoji},
            "color": "gray_background",
            "rich_text": [{"type": "text", "text": {"content": texto, "link": {"url": url}}}]
        }
    }

def criar_pagina_diaria():
    hoje = datetime.date.today()
    dia_mes = hoje.day
    dia_semana = hoje.weekday() 
    
    data_iso = hoje.strftime("%Y-%m-%d")
    data_br = hoje.strftime("%d/%m/%Y")

    blocos_conteudo = []

    # --- VERIFICAÇÃO 1: MENSAL (Percorre a lista de lembretes do dia) ---
    if dia_mes in LEMBRETES_MENSAIS:
        lista_de_hoje = LEMBRETES_MENSAIS[dia_mes]
        for r in lista_de_hoje:
            blocos_conteudo.append(criar_bloco_aviso(r["mensagem"], r["url"], r["emoji"]))
            print(f"   ✅ Adicionado lembrete mensal: {r['mensagem']}")

    # --- VERIFICAÇÃO 2: SEMANAL ---
    if dia_semana == 4:
        r = AVISO_SEXTA_FEIRA
        blocos_conteudo.append(criar_bloco_aviso(r["mensagem"], r["url"], r["emoji"]))
        print(f"   ✅ Adicionado lembrete de sexta-feira.")

    try:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Data": {"date": {"start": data_iso}},
                "Nome": {"title": [{"text": {"content": data_br}}]}
            },
            children=blocos_conteudo 
        )
        print(f"🚀 Página '{data_br}' criada com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    criar_pagina_diaria()
