from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Discos(db.Model):
    __tablename__ = "discos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "autor": self.autor,
            "ano": self.ano,
            "genero": self.genero,
        }
