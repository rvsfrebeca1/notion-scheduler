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

def buscar_pendencias_ultima_pagina():
    """Busca itens de checklist não marcados na última página criada."""
    try:
        # 1. Busca a última página. 
        # Note que usamos 'databases' (plural) e 'query'
        response = notion.databases.query(
            **{
                "database_id": database_id,
                "sorts": [{"property": "Data", "direction": "descending"}],
                "page_size": 1
            }
        )
        
        results = response.get("results", [])
        if not results:
            print("📭 Nenhuma página encontrada no banco de dados.")
            return []

        ultima_pagina_id = results[0]["id"]
        print(f"📄 Analisando página anterior: {ultima_pagina_id}")
        
        # 2. Busca os blocos (conteúdo) dessa página
        blocos = notion.blocks.children.list(block_id=ultima_pagina_id)
        
        pendencias = []
        for bloco in blocos.get("results", []):
            if bloco["type"] == "to_do":
                # Verificamos se o checkbox está FALSO
                if not bloco["to_do"]["checked"]:
                    # Criamos um novo dicionário de bloco para evitar IDs antigos
                    pendencias.append({
                        "object": "block",
                        "type": "to_do",
                        "to_do": {
                            "rich_text": bloco["to_do"]["rich_text"],
                            "checked": False,
                            "color": bloco["to_do"]["color"]
                        }
                    })
        return pendencias

    except Exception as e:
        print(f"⚠️ Erro detalhado na busca: {type(e).__name__} - {e}")
        return []

def criar_pagina_diaria():
    hoje = datetime.date.today()
    dia_mes = hoje.day
    dia_semana = hoje.weekday() 
    
    data_iso = hoje.strftime("%Y-%m-%d")
    data_br = hoje.strftime("%d/%m/%Y")

    blocos_conteudo = []

    # --- NOVO: BUSCAR PENDÊNCIAS DA PÁGINA ANTERIOR ---
    print("🔍 Buscando tarefas pendentes de ontem...")
    pendencias = buscar_pendencias_ultima_pagina()
    if pendencias:
        # Opcional: Adicionar um divisor ou título para separar as pendências
        blocos_conteudo.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": "📌 Pendências de Ontem"}}]}
        })
        blocos_conteudo.extend(pendencias)
        print(f"   ✅ {len(pendencias)} tarefas migradas.")

    # --- VERIFICAÇÃO 1: MENSAL ---
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
        print(f"❌ Erro ao criar página: {e}")

if __name__ == "__main__":
    criar_pagina_diaria()
