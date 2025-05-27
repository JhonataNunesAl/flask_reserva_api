from flask import Blueprint, request, jsonify,render_template,redirect, url_for
from datetime import datetime
from config import db
from models.salasMODEL import SalaNaoEncontrado, listar_salas, adicionar_sala, atualizar_sala, excluir_sala, sala_por_id

salas_blueprint = Blueprint('salas', __name__)

@salas_blueprint.route('/salas', methods=['GET'])
def get_salas():
    salas = listar_salas()
    return jsonify(salas)

@salas_blueprint.route('/salas', methods=['POST'])
def create_sala():
    nova_sala = request.json
    try:
        adicionar_sala(nova_sala)
        return jsonify(nova_sala), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@salas_blueprint.route('/salas/<int:id_sala>', methods=['PUT'])
def update_sala(id_sala):
        data = request.json
        try:
            sala = sala_por_id(id_sala)
            if not sala:
                return jsonify({'message': 'Sala não encontrado'}), 404
            atualizar_sala(id_sala, data)
            
            return jsonify(data),200
        except SalaNaoEncontrado:
            return jsonify({'message': 'Sala não encontrado'}), 404
   
@salas_blueprint.route('/salas/<int:id_sala>', methods=['DELETE'])
def delete_sala(id_sala):
        try:
            excluir_sala(id_sala)
            return jsonify({'message': 'Sala excluído com sucesso '}),200
        except SalaNaoEncontrado:
            return jsonify({'message': 'Sala não encontrado'}), 404