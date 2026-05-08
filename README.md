# Evolution API MCP

MCP server para enviar e receber mensagens no WhatsApp direto do Claude Code, usando [Evolution API](https://github.com/EvolutionAPI/evolution-api) (open-source, self-hosted).

## O que faz

- Criar e gerenciar instancias WhatsApp
- Enviar mensagens de texto, midia, audio, localizacao, contatos, enquetes, stickers, botoes e listas
- Ler conversas e mensagens recebidas
- Reagir a mensagens, arquivar chats, marcar como lido

## Pre-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (gerenciador de pacotes Python)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

## Instalacao

### 1. Subir a Evolution API

```bash
git clone https://github.com/SEU_USUARIO/evolution-api-mcp.git
cd evolution-api-mcp
docker compose up -d
```

Aguarde uns 15 segundos e teste:

```bash
curl http://localhost:8080/
```

Deve retornar `{"status":200,"message":"Welcome to the Evolution API, it is working!"}`.

### 2. Instalar o MCP server

```bash
uv venv
uv pip install -e .
```

### 3. Registrar no Claude Code

```bash
claude mcp add evolution-api -s user -- evolution-api-mcp
```

Ou adicione manualmente no arquivo `~/.claude.json`:

```json
{
  "mcpServers": {
    "evolution-api": {
      "type": "stdio",
      "command": "evolution-api-mcp",
      "env": {
        "EVOLUTION_API_URL": "http://localhost:8080",
        "EVOLUTION_API_KEY": "evo_mcp_2024"
      }
    }
  }
}
```

> **Windows:** o command pode precisar ser o caminho completo do `.exe`:
> `C:/Users/SEU_USUARIO/evolution-api-mcp/.venv/Scripts/evolution-api-mcp.exe`

### 4. Conectar seu WhatsApp

1. Abra http://localhost:8080/manager/ no navegador
2. Use a Global API Key: `evo_mcp_2024`
3. Crie uma instancia (ex: "meuwhats")
4. Clique em "Gerar QR Code"
5. Escaneie com seu WhatsApp: **Configuracoes > Aparelhos conectados > Conectar dispositivo**

### 5. Usar!

Reabra o Claude Code e comece a usar:

```
> envia uma mensagem pro 5511999999999 dizendo oi
> mostra minhas conversas recentes
> envia uma foto pra fulano
```

## Configuracao

| Variavel | Descricao | Default |
|---|---|---|
| `EVOLUTION_API_URL` | URL da Evolution API | `http://localhost:8080` |
| `EVOLUTION_API_KEY` | API key de autenticacao | (vazio) |

A API key padrao do Docker Compose e `evo_mcp_2024`. Mude no `docker-compose.yml` se quiser.

## Estrutura

```
evolution-api-mcp/
├── docker-compose.yml          # Evolution API + PostgreSQL
├── pyproject.toml               # Dependencias Python
└── src/evolution_api_mcp/
    ├── server.py                # MCP server (FastMCP + CodeMode)
    ├── client.py                # HTTP client async
    └── tools/
        ├── instance.py          # Criar/conectar/deletar instancias
        ├── messages.py          # Enviar texto, midia, audio, etc.
        └── chat.py              # Listar chats, ler mensagens
```

## Tools disponiveis

### Instance
- `create_instance` - Criar instancia WhatsApp
- `connect_instance` - Conectar e gerar QR code
- `fetch_instances` - Listar instancias
- `connection_state` - Verificar estado da conexao
- `logout_instance` - Desconectar WhatsApp
- `restart_instance` - Reiniciar instancia
- `delete_instance` - Deletar instancia

### Messages
- `send_text` - Enviar texto
- `send_media` - Enviar imagem, video ou documento
- `send_audio` - Enviar audio/nota de voz
- `send_location` - Enviar localizacao
- `send_contact` - Enviar cartao de contato
- `send_reaction` - Reagir com emoji
- `send_poll` - Enviar enquete
- `send_buttons` - Enviar botoes interativos
- `send_list` - Enviar lista interativa
- `send_sticker` - Enviar sticker

### Chat
- `find_chats` - Listar conversas
- `find_messages` - Ler mensagens de um chat
- `archive_chat` - Arquivar/desarquivar chat
- `mark_message_as_read` - Marcar como lido

## Licenca

MIT
