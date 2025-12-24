import os
import datetime
import calendar
from notion_client import Client

# --- CONFIGURAÇÕES ---
notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")

notion = Client(auth=notion_token)

# 1. RECORRENTE MENSAL: Aparece todo mês no dia X
LEMBRETES_MENSAIS = {
    30: [
        {
            "mensagem": "E, ai. Vamos revisar as metas de 2026 e ver o que ainda faz sentido ou não? Seja sincera consigo mesma!",
            "url": "https://www.notion.so/Vida-Metas-2026-2d16877ef64580d6b820ccc46816102d",
            "emoji": "⚠️"
        }
    ]
}

# 2. ESPECÍFICO ANUAL: (Mês, Dia) - Aparece só uma vez por ano
LEMBRETES_ANUAIS = {
    (3, 30): [{"mensagem": "Fim do primeiro trimestre do ano! Vamos dar uma olhada nas metas desse trimestre", "url": "https://www.notion.so/1-Trimestre-2d16877ef645812891f7fd9805a0756d", "emoji": "✅"}],
    (6, 30): [{"mensagem": "Fim do segundo trimestre do ano! Vamos dar uma olhada nas metas desse trimestre", "url": "https://www.notion.so/2-Trimestre-2d16877ef64581d4aa52c21bcd63df3c", "emoji": "✅"}],
    (9, 30): [{"mensagem": "Fim do terceiro trimestre do ano! Vamos dar uma olhada nas metas desse trimestre", "url": "https://www.notion.so/3-Trimestre-2d16877ef6458117a494c05d4c34e993", "emoji": "✅"}],
    (12, 30): [{"mensagem": "Fim do quarto trimestre do ano! Vamos dar uma olhada nas metas desse trimestre", "url": "https://www.notion.so/4-Trimestre-2d16877ef64581a190e0cc032d0e0b18", "emoji": "✅"}]
}

# 3. SEMANAL: Baseado no dia da semana
AVISO_SEXTA_FEIRA = {
    "mensagem": "Sextou! Preencha o relatório semanal e lembre-se de curtir o final de semana com responsabilidade",
    "url": "https://www.notion.so/H-BITOS-Rotina-saud-vel-2cc6877ef6458050a7d4f1f955a08671",
    "emoji": "🍺"
}

def eh_ultimo_dia_do_mes(data):
    """Retorna True se a data fornecida for o último dia do mês atual."""
    ultimo_dia = calendar.monthrange(data.year, data.month)[1]
    return data.day == ultimo_dia

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
    mes_atual = hoje.month
    dia_semana = hoje.weekday()
    
    data_iso = hoje.strftime("%Y-%m-%d")
    data_br = hoje.strftime("%d/%m/%Y")

    blocos_conteudo = []

    # --- VERIFICAÇÃO 1: MENSAL ---
    if dia_mes in LEMBRETES_MENSAIS:
        for r in LEMBRETES_MENSAIS[dia_mes]:
            blocos_conteudo.append(criar_bloco_aviso(r["mensagem"], r["url"], r["emoji"]))
            print(f"✅ Adicionado lembrete mensal do dia {dia_mes}")

    # --- VERIFICAÇÃO EXTRA: ÚLTIMO DIA DO MÊS ---
    # Se hoje é o último dia mas não é dia 30 (ex: 28 de Fev), 
    # você pode forçar os lembretes do dia 30 a aparecerem aqui.
    if eh_ultimo_dia_do_mes(hoje) and dia_mes < 30:
        if 30 in LEMBRETES_MENSAIS:
            for r in LEMBRETES_MENSAIS[30]:
                blocos_conteudo.append(criar_bloco_aviso(f"[FECHAMENTO] {r['mensagem']}", r["url"], r["emoji"]))
            print(f"📅 Adicionado lembretes de fechamento (último dia do mês).")

    # --- VERIFICAÇÃO 2: ANUAL ---
    data_chave = (mes_atual, dia_mes)
    if data_chave in LEMBRETES_ANUAIS:
        for r in LEMBRETES_ANUAIS[data_chave]:
            blocos_conteudo.append(criar_bloco_aviso(r["mensagem"], r["url"], r["emoji"]))
            print(f"✨ Adicionado lembrete anual: {data_br}")

    # --- VERIFICAÇÃO 3: SEMANAL ---
    if dia_semana == 4: # Sexta-feira
        r = AVISO_SEXTA_FEIRA
        blocos_conteudo.append(criar_bloco_aviso(r["mensagem"], r["url"], r["emoji"]))
        print(f"✅ Adicionado lembrete de sexta-feira.")

    # --- CRIAÇÃO NO NOTION ---
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
