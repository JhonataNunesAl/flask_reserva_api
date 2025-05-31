from flask import Blueprint, request, jsonify
from models.salasMODEL import SalaNaoEncontrado, listar_salas, adicionar_sala, atualizar_sala, excluir_sala, sala_por_id

salas_blueprint = Blueprint('salas', __name__)

@salas_blueprint.route('/salas', methods=['GET'])
def get_salas():
    """
    Get all salas
    ---
    tags:
      - Salas
    responses:
      200:
        description: Lista de todas as salas
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  turma_id:
                    type: integer
                  aula:
                    type: string
    """
    salas = listar_salas()
    return jsonify(salas)

@salas_blueprint.route('/salas', methods=['POST'])
def create_sala():
    """
    Cria uma nova sala
    ---
    tags:
      - Salas
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - turma_id
              - aula
            properties:
              turma_id:
                type: integer
              aula:
                type: string
    responses:
      201:
        description: Sala criada com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                turma_id:
                  type: integer
                aula:
                  type: string
      400:
        description: Erro ao criar sala (já existe)
        content:
          application/json:
            schema:
              type: object
              properties:
                erro:
                  type: string
    """
    nova_sala = request.json
    try:
        adicionar_sala(nova_sala)
        return jsonify(nova_sala), 201
    
    except SalaNaoEncontrado as e:
        return jsonify({"erro": str(e)}), 400


@salas_blueprint.route('/salas/<int:id_sala>', methods=['PUT'])
def update_sala(id_sala):
    """
    Atualiza uma sala pelo ID
    ---
    tags:
      - Salas
    parameters:
      - in: path
        name: id_sala
        schema:
          type: integer
        required: true
        description: ID da sala a ser atualizada
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - turma_id
              - aula
            properties:
              turma_id:
                type: integer
              aula:
                type: string
    responses:
      200:
        description: Sala atualizada com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                turma_id:
                  type: integer
                aula:
                  type: string
      404:
        description: Sala não encontrada ou erro
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    data = request.json
    try:
        sala = sala_por_id(id_sala)
        if not sala:
            return jsonify({'message': 'Sala não encontrado'}), 404
        atualizar_sala(id_sala, data)
        
        return jsonify(data), 200
    except SalaNaoEncontrado as e:
        return jsonify({'message': str(e)}), 404
   
@salas_blueprint.route('/salas/<int:id_sala>', methods=['DELETE'])
def delete_sala(id_sala):
    """
    Exclui uma sala pelo ID
    ---
    tags:
      - Salas
    parameters:
      - in: path
        name: id_sala
        schema:
          type: integer
        required: true
        description: ID da sala a ser excluída
    responses:
      200:
        description: Sala excluída com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Sala não encontrada
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    try:
        excluir_sala(id_sala)
        return jsonify({'message': 'Sala excluído com sucesso '}), 200
    except SalaNaoEncontrado:
        return jsonify({'message': 'Sala não encontrado'}), 404
