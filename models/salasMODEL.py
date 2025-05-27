from datetime import datetime, date
from config import db


class SalaNaoEncontrado(Exception):
    pass

class Salas(db.Model):
    __tablename__ = "salas"
    
    id = db.Column(db.Integer, primary_key=True)
    turma_id = db.Column(db.Integer, nullable=False)
    aula = db.Column(db.String(100), nullable=False)

    def __init__(self, turma_id, aula):
        self.turma_id = turma_id
        self.aula = aula

    def to_dict(self):
        return {
            'id': self.id,
            'turma_id': self.turma_id,
            'aula': self.aula
        }

def listar_salas():
    salas = Salas.query.all()
    return [sala.to_dict() for sala in salas]

def sala_por_id(id_sala):
    sala = Salas.query.get(id_sala)
    if not sala:
        raise SalaNaoEncontrado(f'Sala não encontrado.')
    return sala.to_dict()

def adicionar_sala(nova_sala):
    turma_id=int(nova_sala['turma_id'])
    salas = Salas.query.all()
    for sala in salas:
        if sala.turma_id == nova_sala['turma_id'] and sala.aula == nova_sala['aula']:
            raise SalaNaoEncontrado(f'Sala já existe para a turma {nova_sala["turma_id"]} na aula {nova_sala["aula"]}.')
    
    nova_sala = Salas(
        turma_id=int(nova_sala['turma_id']),
        aula=nova_sala['aula']       
    )

    db.session.add(nova_sala)
    db.session.commit()
    return {"message": "Sala adicionada com sucesso!"}, 201

def atualizar_sala(id_sala, nova_sala):
    sala = Salas.query.get(id_sala)
    if not sala:
        raise SalaNaoEncontrado
    
    salas = Salas.query.all()
    for sala_for in salas:
        if sala_for.turma_id == nova_sala['turma_id'] and sala_for.aula == nova_sala['aula']:
            raise SalaNaoEncontrado(f'Sala já existe para a turma {nova_sala["turma_id"]} na aula {nova_sala["aula"]}.')

    sala.aula = nova_sala['aula']
    sala.turma_id = nova_sala['turma_id']
    
    db.session.commit()
    return {"message": "Sala atualizado com sucesso!"}, 200

def excluir_sala(id_sala):
    sala = Salas.query.get(id_sala)
    if not sala:
        raise SalaNaoEncontrado(f'Sala não encontrado.')

    db.session.delete(sala)
    db.session.commit()
    return {"message": "Sala excluida com sucesso!"}, 200
