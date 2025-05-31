# Orientações para o Chatbot de Montagem de PC Gamer

Este documento fornece instruções para configurar e executar o chatbot especializado em auxiliar na escolha de peças para montar um PC gamer com base nos jogos preferidos e orçamento do usuário.

## Pré-requisitos

Antes de começar, certifique-se de ter o Python 3 instalado em seu sistema. Você também precisará das seguintes bibliotecas:

```bash
pip install Flask flask-cors
```

## Arquivos do Projeto

O projeto consiste em três arquivos principais:
- `chatbot_server.py`: Código do servidor backend que gerencia o fluxo de diálogo
- `qa_data.json`: Arquivo JSON contendo todas as perguntas, respostas e fluxo de escolha
- `index.html`: Interface web temática para interação com o chatbot

## Estrutura do Arquivo JSON

O arquivo `pc_gamer_qa_data.json` contém todo o fluxo de diálogo do chatbot, organizado como pares de perguntas e respostas:

```json
{
    "perguntas_respostas": {
        "comando1": "resposta1",
        "comando2": "resposta2 com\nmúltiplas linhas",
        "comando3": "resposta3 com lista:\n- Item 1\n- Item 2"
    }
}
```

### Fluxo de Diálogo

O chatbot foi projetado com um fluxo de diálogo estruturado:

1. **Início**: O usuário começa com "montar pc" ou outro comando inicial
2. **Tipo de Jogos**: O usuário escolhe entre "jogos pesados", "jogos leves" ou "ambos"
3. **Jogos Específicos**: O usuário seleciona jogos específicos (GTA, CS, etc.)
4. **Orçamento**: O usuário define seu orçamento (baixo, médio, alto)
5. **Recomendação**: O chatbot apresenta uma configuração recomendada
6. **Detalhes/Finalização**: O usuário pode solicitar mais detalhes ou finalizar

## Executando o Servidor Backend

1. **Navegue até o diretório:** Abra seu terminal ou prompt de comando e navegue até o diretório onde você salvou os arquivos.
2. **Execute o script Python:** Digite o seguinte comando e pressione Enter:

   ```bash
   python chatbot_server.py
   ```

3. **Servidor Ativo:** Você verá mensagens indicando que o servidor Flask foi iniciado e está rodando em `http://127.0.0.1:5000`. O servidor agora está pronto para receber requisições.

## Acessando a Interface Web

1. **Abra o arquivo HTML:** Após iniciar o servidor, abra o arquivo `index.html` em seu navegador web. Você pode fazer isso de duas maneiras:
   - Clique duas vezes no arquivo `index.html` para abri-lo diretamente no navegador
   - Ou digite o caminho completo do arquivo na barra de endereços do navegador (ex: `file:///caminho/para/seu/index.html`)

2. **Interagindo com o Chatbot:** A interface web apresenta:
   - Uma caixa de mensagens onde as conversas serão exibidas
   - Chips de sugestão que mudam dinamicamente com base no contexto da conversa
   - Uma caixa de texto para digitar comandos personalizados
   - Um botão "Enviar" para enviar suas mensagens

## Personalizando o Chatbot

### Modificando o Fluxo de Diálogo

Para personalizar o fluxo de diálogo, edite o arquivo `qa_data.json`. Você pode:

1. **Adicionar novos comandos e respostas**:
   ```json
   "novo comando": "Nova resposta com opções:\n- Opção A\n- Opção B"
   ```

2. **Modificar recomendações existentes**:
   ```json
   "orçamento baixo": "Configuração atualizada para orçamento baixo:\n**Processador:** [novo processador]\n**Placa de vídeo:** [nova placa]"
   ```

3. **Adicionar novos jogos ou categorias**:
   ```json
   "novo jogo": "Informações sobre o novo jogo...\n\nQual é o seu orçamento aproximado?\n- Digite 'orçamento baixo'\n- Digite 'orçamento médio'\n- Digite 'orçamento alto'"
   ```

### Formatação de Texto

O chatbot suporta formatação básica no arquivo JSON:

- **Quebras de linha**: Use `\n` para inserir uma quebra de linha
- **Listas**: Use `\n- ` para criar itens de lista
- **Destaque**: Use `**texto**` para destacar componentes importantes (aparecerão em roxo na interface)

### Atualizando as Sugestões na Interface

A interface web atualiza automaticamente as sugestões com base no contexto da conversa. Se você adicionar novos comandos ao JSON, pode ser necessário atualizar a função `updateSuggestions()` no arquivo HTML para incluir esses novos comandos nas sugestões dinâmicas.

## Exemplo de Uso

1. Usuário clica em "montar pc"
2. Chatbot apresenta opções de tipos de jogos
3. Usuário seleciona "jogos pesados"
4. Chatbot pergunta sobre jogos específicos
5. Usuário seleciona "gta"
6. Chatbot pergunta sobre orçamento
7. Usuário seleciona "orçamento médio"
8. Chatbot apresenta configuração recomendada
9. Usuário pode solicitar "detalhes" ou "finalizar"

## Solução de Problemas

1. **Erro "Address already in use":** Se o servidor não iniciar devido a um erro indicando que a porta já está em uso, verifique se não há outra instância do servidor rodando. Você pode encerrar processos Python existentes ou alterar a porta no arquivo `chatbot_server.py`.

2. **Erro de CORS:** Se o navegador mostrar erros relacionados a CORS no console, verifique se você está usando o arquivo `chatbot_server.py` que inclui suporte a CORS.

3. **Formatação incorreta:** Se a formatação (como destaque de texto ou quebras de linha) não estiver funcionando corretamente, verifique se o JSON está corretamente formatado e se o HTML está processando as tags de formatação.

4. **Sugestões não atualizando:** Se as sugestões não estiverem atualizando corretamente com base no contexto, verifique a função `updateSuggestions()` no arquivo HTML.
