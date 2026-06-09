from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
import json
import os
import anthropic
from collections import defaultdict

load_dotenv()

app = Flask(__name__)
CORS(app)  # NOSONAR — intentional; file:// origin requires permissive CORS for local dev

# In-memory conversation history keyed by session_id
conversation_histories: dict[str, list] = defaultdict(list)


def load_knowledge_base() -> dict:
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qa_data.json')
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f).get('perguntas_respostas', {})
    except Exception as e:
        print(f"Erro ao carregar qa_data.json: {e}")
        return {}


def build_system_prompt() -> str:
    kb = load_knowledge_base()
    kb_text = json.dumps(kb, ensure_ascii=False, indent=2)

    intro = (
        "Você é o PC Builder Bot, um assistente especializado em ajudar pessoas a montarem PCs gamers no Brasil.\n\n"
        "Seu objetivo é recomendar configurações de hardware com base nos jogos favoritos e orçamento do usuário.\n\n"
        "Use a base de conhecimento abaixo como referência de fluxo e recomendações:\n\n"
    )
    instructions = (
        "\n\nInstruções:\n"
        "- Responda sempre em português brasileiro\n"
        "- Seja amigável, direto e prestativo\n"
        "- Use **negrito** para destacar nomes de componentes de hardware (CPU, GPU, etc.)\n"
        "- Você pode expandir as respostas com conhecimento técnico atualizado\n"
        "- Orçamentos estão em Reais (R$)\n"
        "- Ao recomendar uma build, sempre inclua: CPU, GPU, RAM, Armazenamento, Placa-mãe e Fonte\n"
        "- Você pode responder perguntas livres sobre hardware, não apenas os comandos pré-definidos\n"
        "- Mantenha o contexto da conversa para dar respostas coerentes"
    )
    return intro + f"<knowledge_base>\n{kb_text}\n</knowledge_base>" + instructions


@app.route('/chat', methods=['POST'])
def chat():
    """Stream a Claude response for the given message."""
    try:
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')

        if not user_message:
            return jsonify({"error": "Mensagem vazia"}), 400

        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return jsonify({"error": "ANTHROPIC_API_KEY não configurada no servidor."}), 500

        client = anthropic.Anthropic(api_key=api_key)

        conversation_histories[session_id].append({"role": "user", "content": user_message})
        # Keep last 20 messages to stay within context limits
        history = conversation_histories[session_id][-20:]

        def generate():
            full_response = ""
            try:
                with client.messages.stream(
                    model="claude-opus-4-8",
                    max_tokens=2048,
                    system=build_system_prompt(),
                    messages=history,
                ) as stream:
                    for text in stream.text_stream:
                        full_response += text
                        yield f"data: {json.dumps({'text': text})}\n\n"

                conversation_histories[session_id].append(
                    {"role": "assistant", "content": full_response}
                )
                yield f"data: {json.dumps({'done': True})}\n\n"

            except anthropic.AuthenticationError:
                yield f"data: {json.dumps({'error': 'Chave da API inválida. Verifique ANTHROPIC_API_KEY.'})}\n\n"
            except Exception as e:
                print(f"Erro na stream: {e}")
                yield f"data: {json.dumps({'error': 'Erro ao processar resposta.'})}\n\n"

        return Response(
            stream_with_context(generate()),
            content_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Access-Control-Allow-Origin': '*',
            },
        )

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"error": "Erro interno do servidor."}), 500


@app.route('/reset', methods=['POST'])
def reset():
    """Clear conversation history for a session."""
    data = request.get_json() or {}
    session_id = data.get('session_id', 'default')
    conversation_histories[session_id] = []
    return jsonify({"message": "Conversa reiniciada"})


if __name__ == '__main__':
    import threading
    import webbrowser

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("⚠️  AVISO: ANTHROPIC_API_KEY não está configurada!")
        print("   Windows: set ANTHROPIC_API_KEY=sua_chave_aqui")
        print("   Linux/Mac: export ANTHROPIC_API_KEY=sua_chave_aqui")
    else:
        print("✓ ANTHROPIC_API_KEY encontrada")

    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    url = f'file:///{html_path.replace(os.sep, "/")}'
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    print("\n🎮 PC Builder Bot iniciado em http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)
