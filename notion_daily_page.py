import os
from notion_client import Client
import datetime

# Configurações iniciais
notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("DATABASE_ID")

# Verificação de segurança simples
if not notion_token or not database_id:
    raise ValueError("Por favor, configure as variáveis de ambiente NOTION_TOKEN e DATABASE_ID.")

notion = Client(auth=notion_token)

# --- CONFIGURAÇÃO DE LEMBRETES ---
# Dicionário onde a CHAVE é o dia do mês e o VALOR é o lembrete e o link.
# Você pode adicionar quantos dias quiser aqui.
LEMBRETES = {
    17: {
        "mensagem": "Hoje é dia 30! Não esqueça de preencher o checklist de juntar grana 💰",
        "url": "https://www.notion.so/H-BITO-Juntar-dinheiro-mensalmente-2cc6877ef64580df94cfe074814f71b3" 
    },
    17: {
        "mensagem": "Dia 5: Hora de revisar as metas mensais! 🎯",
        "url": "https://www.notion.so/1f86877ef64581cbb510df4b617a898e?v=1f86877ef64581db8965000c4e063372"
    }
}

def criar_pagina_diaria():
    hoje = datetime.date.today()
    dia_atual = hoje.day # Ex: 30
    
    data_formatada_iso = hoje.strftime("%Y-%m-%d")
    data_formatada_br = hoje.strftime("%d/%m/%Y")

    print(f"📅 Iniciando criação para: {data_formatada_br}")

    # 1. Definir as propriedades básicas (Metadados da página)
    propriedades = {
        "Data": {"date": {"start": data_formatada_iso}},
        "Nome": {"title": [{"text": {"content": data_formatada_br}}]}
    }

    # 2. Definir o conteúdo da página (Blocos internos)
    blocos_conteudo = []

    # Verifica se existe um lembrete para o dia de hoje
    if dia_atual in LEMBRETES:
        info_lembrete = LEMBRETES[dia_atual]
        
        # Cria um bloco de destaque (Callout) com link
        bloco_lembrete = {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"emoji": "🔔"},
                "color": "gray_background",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": info_lembrete["mensagem"],
                            "link": {"url": info_lembrete["url"]} # Aqui vai o link clicável
                        }
                    }
                ]
            }
        }
        blocos_conteudo.append(bloco_lembrete)
        print(f"💡 Lembrete encontrado e adicionado para o dia {dia_atual}.")

    # 3. Enviar para o Notion
    try:
        nova_pagina = notion.pages.create(
            parent={"database_id": database_id},
            properties=propriedades,
            children=blocos_conteudo # Adiciona os blocos aqui
        )
        print(f"🚀 Página '{data_formatada_br}' criada com sucesso! ID: {nova_pagina['id']}")
        
    except Exception as e:
        print(f"❌ Erro ao criar a página: {e}")

if __name__ == "__main__":
    criar_pagina_diaria()
