from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

def carregar_qa():
    """Carrega as perguntas e respostas do arquivo JSON."""
    try:
        caminho_arquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qa_data.json')
        
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            return dados.get('perguntas_respostas', {})
    except Exception as e:
        print(f"Erro ao carregar o arquivo JSON: {e}")
        return {}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        qa_pairs = carregar_qa()
        
        user_message = request.json.get('message', '').lower().strip()
        
        response = qa_pairs.get(user_message, "Desculpe, não entendi essa pergunta. Digite 'ajuda' para ver os comandos disponíveis.")
        
        return jsonify({"response": response})
    except Exception as e:
        print(f"Erro ao processar a requisição: {e}")
        return jsonify({"error": "Ocorreu um erro interno no servidor."}), 500

if __name__ == '__main__':
    # Executa o servidor na rede local
    print("Servidor chatbot PC Gamer iniciado em http://127.0.0.1:5000")
    print("Use POST para /chat com JSON {'message': 'sua_pergunta'} para interagir.")
    print(f"Carregando perguntas e respostas do arquivo 'pc_gamer_qa_data.json'...")
    
    # Carrega e exibe as perguntas disponíveis
    qa_pairs = carregar_qa()
    if qa_pairs:
        print(f"Comandos disponíveis: {', '.join(qa_pairs.keys())}")
    else:
        print("Aviso: Nenhuma pergunta e resposta foi carregada do arquivo JSON.")
    
    app.run(host='127.0.0.1', port=5000, debug=False)
