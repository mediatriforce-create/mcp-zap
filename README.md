# Evolution API MCP

MCP server para enviar e receber mensagens no WhatsApp direto do Claude Code, usando [Evolution API](https://github.com/EvolutionAPI/evolution-api) (open-source, self-hosted).

## O que faz

- Criar e gerenciar instancias WhatsApp
- Enviar mensagens de texto, midia, audio, localizacao, contatos, enquetes, stickers, botoes e listas
- Ler conversas e mensagens recebidas
- Reagir a mensagens, arquivar chats, marcar como lido

---

## Opcao A — Railway (recomendado, sem Docker)

Deploy em nuvem em 5 minutos. Nao precisa de Docker nem servidor local.

### 1. Criar conta no Railway

Acesse [railway.com](https://railway.com) e crie uma conta gratuita.

### 2. Deploy do template Evolution API

1. No Railway, clique em **New Project**
2. Clique em **Deploy a template**
3. Pesquise **Evolution API** (o template com mais de 2000 projetos — tem Postgres + Redis inclusos)
4. Clique em **Deploy**
5. Aguarde ~2 minutos ate todos os servicos ficarem `Active`

### 3. Gerar dominio publico

1. Clique no servico **Evolution API**
2. Va em **Settings** → **Networking** → **Generate Domain**
3. Anote a URL gerada (ex: `evolution-api-production-xxxx.up.railway.app`)

### 4. Configurar API Key

No servico **Evolution API**, va em **Variables** e adicione:

| Variavel | Valor |
|---|---|
| `AUTHENTICATION_TYPE` | `apikey` |
| `AUTHENTICATION_API_KEY` | Uma chave forte (ex: gere com `openssl rand -hex 16`) |

Clique em **Deploy** para aplicar.

### 5. Criar instancia e escanear QR

```bash
# Criar instancia
curl -X POST "https://SUA-URL.up.railway.app/instance/create" \
  -H "apikey: SUA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"instanceName":"meuwhats","integration":"WHATSAPP-BAILEYS","qrcode":true}'

# Pegar QR code (rode e escaneie com o WhatsApp)
curl "https://SUA-URL.up.railway.app/instance/connect/meuwhats" \
  -H "apikey: SUA_API_KEY"
```

O campo `base64` da resposta e a imagem do QR. Salve e abra:

```bash
# Salvar QR como imagem e abrir
curl "https://SUA-URL.up.railway.app/instance/connect/meuwhats" \
  -H "apikey: SUA_API_KEY" | python3 -c "
import json,sys,base64
d=json.load(sys.stdin)
b64=d['base64'].replace('data:image/png;base64,','')
open('qr.png','wb').write(base64.b64decode(b64))
print('QR salvo em qr.png')
"
open qr.png   # macOS
# start qr.png  # Windows
```

Escaneie com seu WhatsApp: **Configuracoes > Aparelhos conectados > Conectar dispositivo**

### 6. Instalar o MCP server

```bash
git clone https://github.com/SEU_USUARIO/mcp-zap.git
cd mcp-zap
uv venv
uv pip install -e .
```

### 7. Registrar no Claude Code

Edite `~/.claude.json` e adicione dentro de `mcpServers`:

```json
{
  "mcpServers": {
    "evolution-api": {
      "type": "stdio",
      "command": "evolution-api-mcp",
      "env": {
        "EVOLUTION_API_URL": "https://SUA-URL.up.railway.app",
        "EVOLUTION_API_KEY": "SUA_API_KEY",
        "EVOLUTION_INSTANCE": "meuwhats"
      }
    }
  }
}
```

> **Windows:** use o caminho completo do `.exe`:
> `"command": "C:/Users/SEU_USUARIO/mcp-zap/.venv/Scripts/evolution-api-mcp.exe"`

Reabra o Claude Code e pronto.

---

## Opcao B — Docker local

Para quem prefere rodar tudo na propria maquina.

### Pre-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

### 1. Subir a Evolution API

```bash
git clone https://github.com/SEU_USUARIO/mcp-zap.git
cd mcp-zap
docker compose up -d
```

Aguarde ~15 segundos e teste:

```bash
curl http://localhost:8080/
# {"status":200,"message":"Welcome to the Evolution API, it is working!"}
```

### 2. Conectar seu WhatsApp

1. Acesse `http://localhost:8080/manager/`
2. Use a API Key: `evo_mcp_2024`
3. Crie uma instancia (ex: `meuwhats`)
4. Clique em **Gerar QR Code** e escaneie

### 3. Instalar e registrar o MCP

```bash
uv venv
uv pip install -e .
```

Edite `~/.claude.json`:

```json
{
  "mcpServers": {
    "evolution-api": {
      "type": "stdio",
      "command": "evolution-api-mcp",
      "env": {
        "EVOLUTION_API_URL": "http://localhost:8080",
        "EVOLUTION_API_KEY": "evo_mcp_2024",
        "EVOLUTION_INSTANCE": "meuwhats"
      }
    }
  }
}
```

> **Windows:** use o caminho completo: `C:/Users/SEU_USUARIO/mcp-zap/.venv/Scripts/evolution-api-mcp.exe`

---

## Usando

Apos configurar, reabra o Claude Code:

```
> envia uma mensagem pro 5511999999999 dizendo oi
> mostra minhas conversas recentes
> qual foi a ultima mensagem do fulano?
```

---

## Configuracao

| Variavel | Descricao | Exemplo |
|---|---|---|
| `EVOLUTION_API_URL` | URL da Evolution API | `https://xxxx.up.railway.app` ou `http://localhost:8080` |
| `EVOLUTION_API_KEY` | API key de autenticacao | `96CF28F9329F-44A3-80DB-5190D7B27185` |
| `EVOLUTION_INSTANCE` | Nome da instancia criada | `meuwhats` |

---

## Estrutura

```
mcp-zap/
├── docker-compose.yml          # Evolution API + PostgreSQL (opcao local)
├── pyproject.toml              # Dependencias Python
└── src/evolution_api_mcp/
    ├── server.py               # MCP server (FastMCP + CodeMode)
    ├── client.py               # HTTP client async
    └── tools/
        ├── instance.py         # Criar/conectar/deletar instancias
        ├── messages.py         # Enviar texto, midia, audio, etc.
        └── chat.py             # Listar chats, ler mensagens
```

## Tools disponiveis

### Instance
- `create_instance` — Criar instancia WhatsApp
- `connect_instance` — Conectar e gerar QR code
- `fetch_instances` — Listar instancias
- `connection_state` — Verificar estado da conexao
- `logout_instance` — Desconectar WhatsApp
- `restart_instance` — Reiniciar instancia
- `delete_instance` — Deletar instancia

### Messages
- `send_text` — Enviar texto
- `send_media` — Enviar imagem, video ou documento
- `send_audio` — Enviar audio/nota de voz
- `send_location` — Enviar localizacao
- `send_contact` — Enviar cartao de contato
- `send_reaction` — Reagir com emoji
- `send_poll` — Enviar enquete
- `send_buttons` — Enviar botoes interativos
- `send_list` — Enviar lista interativa
- `send_sticker` — Enviar sticker

### Chat
- `find_chats` — Listar conversas
- `find_messages` — Ler mensagens de um chat
- `archive_chat` — Arquivar/desarquivar chat
- `mark_message_as_read` — Marcar como lido

## Licenca

MIT
