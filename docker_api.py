from flask import Flask, jsonify, request
from flask_cors import CORS

from config import Config
from models import Discos, db

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()


def get_last_id():
    last_disco = Discos.query.order_by(Discos.id.desc()).first()
    return last_disco.id if last_disco else 0


@app.route("/discos", methods=["POST"])
def registrar_disco():
    dados = request.get_json()

    if not isinstance(dados, dict):
        return jsonify({"error": "Invalid data format. Expected a JSON object."}), 400

    lastid = get_last_id()
    try:
        novo_disco = Discos(
            id=lastid + 1,
            nome=dados.get("nome"),
            autor=dados.get("autor"),
            ano=dados.get("ano"),
            genero=dados.get("genero"),
        )
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except TypeError as e:
        return jsonify({"error": f"Type error: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

    db.session.add(novo_disco)
    db.session.commit()
    return jsonify(novo_disco.to_dict()), 201


@app.route("/discos", methods=["GET"])
def listar_discos():
    discos = Discos.query.all()
    return jsonify([u.to_dict() for u in discos]), 200


@app.route("/discos/<int:id>", methods=["GET"])
def pegar_disco(id):
    discos = Discos.query.get_or_404(id)
    return jsonify(discos.to_dict()), 200


@app.route("/discos/<int:id>", methods=["PUT"])
def atualizar_disco(id):
    discos = Discos.query.get_or_404(id)
    dados = request.get_json()
    discos.nome = dados.get("nome", discos.nome)
    discos.autor = dados.get("autor", discos.autor)
    discos.ano = dados.get("ano", discos.ano)
    discos.genero = dados.get("genero", discos.genero)
    db.session.commit()
    return jsonify(discos.to_dict()), 200


@app.route("/discos/<int:id>", methods=["DELETE"])
def deletar_disco(id):
    discos = Discos.query.get_or_404(id)
    db.session.delete(discos)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
