from config import Config
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Discos, db

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/discos", methods=["POST"])
def registrar_disco():
    dados = request.json
    novo_disco = Discos(
        nome=dados["nome"],
        autor=dados["autor"],
        ano=dados["ano"],
        genero=dados["genero"],
    )
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
    dados = request.json
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
    app.run(debug=True)
