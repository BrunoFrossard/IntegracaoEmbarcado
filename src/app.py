from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

try:
    from database import init_db, inserir_leitura, buscar_leituras, buscar_uma_leitura, atualizar_leitura, deletar_leitura
except ImportError:
    print("Erro: Não encontrei o arquivo database.py ou as funções dentro dele.")

app = Flask(__name__)

with app.app_context():
    try:
        init_db()
        print("Sucesso: Banco de dados inicializado e pronto para uso.")
    except Exception as e:
        print(f"Erro ao iniciar banco: {e}")

@app.route('/')
def index():
    """Página principal com os Cards e o Gráfico Real-time"""
    return render_template('index.html')

@app.route('/historico')
def pagina_historico():
    dados = buscar_leituras()
    return render_template('historico.html', leituras=dados)

@app.route('/editar/<int:id_leitura>')
def pagina_editar(id_leitura):
    """Página com formulário para editar um registro específico"""
    leitura = buscar_uma_leitura(id_leitura)
    if leitura:
        return render_template('editar.html', leitura=leitura)
    return "Leitura não encontrada", 404

@app.route('/api/estatisticas')
def api_dados():
    """Rota que o JavaScript do gráfico usa para buscar os dados do banco"""
    try:
        dados = buscar_leituras()
        return jsonify({"historico": dados[-20:]})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/leituras', methods=['POST'])
def nova_leitura():
    """Recebe dados do Arduino (via serial_reader.py) ou Simulador"""
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400
    
    t = dados.get('temperatura')
    u = dados.get('umidade')
    p = dados.get('pressao')
    
    try:
        inserir_leitura(t, u, p)
        print(f"Dado salvo: T:{t} U:{u} P:{p}")
        return jsonify({"status": "sucesso"}), 201
    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")
        return jsonify({"erro": str(e)}), 500

@app.route('/leituras/<int:id_leitura>', methods=['PUT'])
def api_editar_leitura(id_leitura):
    """Atualiza um registro via API"""
    dados = request.get_json()
    try:
        atualizar_leitura(id_leitura, dados['temperatura'], dados['umidade'], dados['pressao'])
        return jsonify({"status": "atualizado"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/leituras/<int:id_leitura>', methods=['DELETE'])
def api_excluir_leitura(id_leitura):
    """Remove um registro via API"""
    try:
        deletar_leitura(id_leitura)
        return jsonify({"status": "removido"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
