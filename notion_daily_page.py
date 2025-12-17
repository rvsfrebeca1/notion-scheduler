import os
from notion_client import Client
import datetime

# --- CONFIGURAÇÕES ---
notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")

if not notion_token or not database_id:
    raise ValueError("Configure as variáveis NOTION_TOKEN e DATABASE_ID.")

notion = Client(auth=notion_token)

# 1. Regras Mensais (Dia do mês -> Aviso)
LEMBRETES_MENSAIS = {
    30: {
        "mensagem": "Hoje é dia de checklist financeiro mensal!",
        "url": "https://www.notion.so/H-BITO-Juntar-dinheiro-mensalmente-2cc6877ef64580df94cfe074814f71b3",
        "emoji": "💰"
    },
    30: {
        "mensagem": "Eai, vamos revisar as metas de 2026 e ver o que ainda faz sentido ou não? Seja sincera consigo mesma!",
        "url": "https://www.notion.so/Planos-pessoais-por-prioridade-7ee8cb657df94cbea68deb61767d904c?source=copy_link#2cc6877ef645806bb8e5c69636afd25b",
        "emoji": "⚠️"
    }
}

# 2. Regras Semanais (Sexta-feira -> Aviso)
# Sexta-feira no Python é representada pelo número 4 (Segunda=0, Dom=6)
AVISO_SEXTA_FEIRA = {
    "mensagem": "Sextou! Preencha e revise as metas antes de curtir o final de semana.",
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
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": texto,
                        "link": {"url": url}
                    }
                }
            ]
        }
    }

def criar_pagina_diaria():
    hoje = datetime.date.today()
    dia_mes = 30  # hoje.day
    dia_semana = 4 # hoje.weekday() # Retorna 0 (seg) a 6 (dom). Sexta é 4.
    
    data_iso = hoje.strftime("%Y-%m-%d")
    data_br = hoje.strftime("%d/%m/%Y")

    print(f"🔄 Processando para: {data_br} (Dia da semana: {dia_semana})")

    # Lista que vai acumular todos os blocos (conteúdo da página)
    blocos_conteudo = []

    # --- VERIFICAÇÃO 1: É dia específico do mês? ---
    if dia_mes in LEMBRETES_MENSAIS:
        rule = LEMBRETES_MENSAIS[dia_mes]
        bloco = criar_bloco_aviso(rule["mensagem"], rule["url"], rule["emoji"])
        blocos_conteudo.append(bloco)
        print(f"   ✅ Adicionado lembrete mensal do dia {dia_mes}")

    # --- VERIFICAÇÃO 2: É Sexta-feira? (4) ---
    if dia_semana == 4:
        bloco = criar_bloco_aviso(
            AVISO_SEXTA_FEIRA["mensagem"], 
            AVISO_SEXTA_FEIRA["url"], 
            AVISO_SEXTA_FEIRA["emoji"]
        )
        blocos_conteudo.append(bloco)
        print(f"   ✅ Adicionado lembrete semanal de Sexta-feira")

    # Monta as propriedades da página
    propriedades = {
        "Data": {"date": {"start": data_iso}},
        "Nome": {"title": [{"text": {"content": data_br}}]}
    }

    try:
        nova_pagina = notion.pages.create(
            parent={"database_id": database_id},
            properties=propriedades,
            children=blocos_conteudo # Envia a lista (pode ter 0, 1 ou 2 itens)
        )
        print(f"🚀 Página '{data_br}' criada com sucesso! ID: {nova_pagina['id']}")
        
    except Exception as e:
        print(f"❌ Erro ao criar a página: {e}")

if __name__ == "__main__":
    criar_pagina_diaria()
