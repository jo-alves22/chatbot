# PC Gamer Builder Bot

Chatbot especializado em recomendar configurações de hardware para PCs gamers no Brasil, alimentado pela API do Claude (Anthropic).

## Como funciona

O bot usa o modelo **claude-opus-4-8** da Anthropic para entender perguntas em linguagem natural. O arquivo `qa_data.json` é embutido no system prompt como base de conhecimento, guiando recomendações de builds, orçamentos em BRL, jogos suportados e periféricos.

## Pré-requisitos

- Python 3.8+
- Chave de API da Anthropic → [console.anthropic.com](https://console.anthropic.com)

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com sua chave de API:

```
ANTHROPIC_API_KEY=sk-ant-...
```

> O arquivo `.env` já está no `.gitignore` — nunca o commite.

## Executando

```bash
python chatbot_server.py
```

O servidor sobe em `http://127.0.0.1:5000` e o `index.html` abre automaticamente no browser padrão.

## Arquivos do projeto

| Arquivo | Descrição |
|---|---|
| `chatbot_server.py` | Servidor Flask com streaming SSE e histórico de conversa |
| `index.html` | Interface web com indicador de digitação e sugestões dinâmicas |
| `qa_data.json` | Base de conhecimento: builds, jogos, orçamentos e guias |
| `requirements.txt` | Dependências Python |
| `.env` | Chave da API (não versionado) |

## Funcionalidades

- **Linguagem natural** — entende perguntas livres, não apenas comandos exatos
- **Streaming** — respostas aparecem progressivamente enquanto o Claude gera
- **Histórico de conversa** — mantém contexto das últimas 20 mensagens por sessão
- **Nova Conversa** — botão no header para reiniciar sem recarregar a página
- **Sugestões dinâmicas** — chips se adaptam ao contexto da conversa

## Base de conhecimento (`qa_data.json`)

O arquivo cobre os seguintes tópicos e pode ser editado livremente:

**Builds por orçamento:**
- Ultra baixo (até R$ 2.500), Baixo (até R$ 5.000), Médio (R$ 5k–R$ 8k), Alto (R$ 8k–R$ 15k), Ultra alto (acima de R$ 15k)

**Jogos suportados:**
- Pesados: Cyberpunk 2077, Elden Ring, Hogwarts Legacy, Black Myth: Wukong, GTA V, RDR2, The Last of Us
- Leves/Esports: CS2, Valorant, League of Legends, Apex Legends, Fortnite, Minecraft, Rainbow Six Siege

**Guias extras:**
- Monitores, periféricos, onde comprar no Brasil, resfriamento, RAM, SSD, upgrade e compatibilidade

## Personalizando

Para atualizar preços, adicionar jogos ou mudar builds, edite o `qa_data.json` — as mudanças são incorporadas automaticamente no próximo start do servidor.

## Solução de problemas

**Porta já em uso:** encerre outros processos Python ou altere a porta em `chatbot_server.py`.

**Erro de CORS:** certifique-se de que o servidor está rodando antes de abrir o `index.html`.

**`ANTHROPIC_API_KEY` não encontrada:** verifique se o arquivo `.env` existe na mesma pasta que `chatbot_server.py`.
