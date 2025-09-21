from flask import Blueprint,jsonify, request,current_app, g
from app.models.usuario import LoginPayload
from app.models.produtos import *
from pydantic import ValidationError
from bson import ObjectId
from app.database import mongo
from bson.json_util import dumps
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt
import logging



main_bp = Blueprint('main_bp',__name__)

#RF: O Sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route('/login',methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        if not raw_data:
            return jsonify({"error": "Request body must be JSON and not empty"}), 400
        user_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    
    if user_data.username == 'admin' and user_data.password == '123':
        
        token = jwt.encode(
            {
                'user_id': user_data.username,
                'exp':datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({'acess_token':token}),200
    
    return jsonify({"error":"Credenciais inválidas"}),401


#RF: O Sistema deve permitir listagem de todos os produtos
@main_bp.route('/produtos',methods=['GET'])
def get_produtos():
    try:
        # Acessando a coleção 'produtos' usando a notação de dicionário para evitar erros de linter.
        produtos_cursor = mongo.db['produtos'].find({})
        # dumps serializa o cursor do MongoDB para uma string JSON, tratando tipos como ObjectId.
        return dumps(produtos_cursor), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

#RF: O Sistema deve permitir a criação de um novo produto
@main_bp.route('/produtos',methods=['POST'])
@token_required
def criar_produtos():
    try:
        produto_data = request.get_json()
        if not produto_data:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Valida e adiciona o ID do usuário (do token) aos dados do produto para auditoria.
        user_id = g.user.get('user_id')
        if not user_id:
            logging.warning("Token payload is missing 'user_id'.")
            return jsonify({"error": "Token inválido: 'user_id' ausente no payload."}), 401
        produto_data['criado_por'] = user_id

        # Valida os dados recebidos (incluindo 'criado_por') com o modelo Pydantic
        produto = Produto(**produto_data)

        # Converte o modelo para um dicionário, usando o alias '_id' e removendo campos nulos
        dados_para_inserir = produto.model_dump(by_alias=True, exclude_none=True)
        # Insere no banco de dados
        result = mongo.db['produtos'].insert_one(dados_para_inserir)
        # Busca o documento recém-criado para retornar na resposta
        novo_produto = mongo.db['produtos'].find_one({"_id": result.inserted_id})
        return dumps(novo_produto), 201, {'Content-Type': 'application/json'}
    except ValidationError as e:
        return jsonify({"error": "Invalid input data", "details": e.errors()}), 400
    except Exception as e:
        logging.error(f"Unexpected error in criar_produtos: {e}", exc_info=True)
        return jsonify({"error": "An unexpected internal error occurred."}), 500

#RF: O Sistema deve permitir a visualização dos detalhes de um produto
@main_bp.route('/produtos/<string:id_produto>',methods=['GET'])
def get_produto_por_id(id_produto):
    try:
        # Converte a string do ID para um ObjectId do MongoDB
        obj_id = ObjectId(id_produto)
    except Exception:
        return jsonify({"error": "Invalid product ID format"}), 400

    produto = mongo.db['produtos'].find_one({"_id": obj_id})
    
    if produto:
        return dumps(produto), 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({"error": "Product not found"}), 404
#RF: O Sistema deve permitir a atualização de um unico produto e prod existente
@main_bp.route('/produtos/<string:id_produto>',methods=['PUT'])
@token_required
def update_produto(id_produto):
    try:
        try:
            oid = ObjectId(id_produto)
        except Exception:
            return jsonify({"error": "Invalid product ID format"}), 400

        update_data_raw = request.get_json()
        if not update_data_raw:
            return jsonify({"error": "Request body must be JSON and not empty"}), 400
        
        # Valida os dados recebidos com o modelo Pydantic
        update_data = UpdateProduto(**update_data_raw)
        # Converte para dict, excluindo campos que não foram enviados no JSON
        dados_para_atualizar = update_data.model_dump(exclude_unset=True)

        if not dados_para_atualizar:
            return jsonify({"error": "No update data provided"}), 400

        update_result = mongo.db['produtos'].update_one(
            {"_id": oid},
            {"$set": dados_para_atualizar}
        )

        if update_result.matched_count == 0:
            return jsonify({"error": "Produto não encontrado"}), 404

        updated_produto = mongo.db['produtos'].find_one({"_id": oid})
        return dumps(updated_produto), 200, {'Content-Type': 'application/json'}
    except ValidationError as e:
        return jsonify({"error": "Invalid input data", "details": e.errors()}), 400
    except Exception as e:
        logging.error(f"Unexpected error in update_produto: {e}", exc_info=True)
        return jsonify({"error": "An unexpected internal error occurred."}), 500
#RF: O Sistema deve permitir a remoção de um unico produto e produto existente
@main_bp.route('/produtos/<string:id_produto>',methods=['DELETE'])
def remove_produto(id_produto):
    try:
        oid = ObjectId(id_produto)
    except Exception:
        return jsonify({"error":"id do produto invalido"}),400
    
    delete_produto = mongo.db['produtos'].delete_one({"_id":oid})

    if delete_produto.deleted_count == 0:
        return jsonify({"error":"Produto não encontrado!"}),404
    
    return "",204
#RF: O Sistema deve permitir a importação de vendas atraves de um arquivo
@main_bp.route('/vendas/upload',methods=['POST'])
def upload_vendas():
    return jsonify({'message':'essa eh a rota de upload de vendas'})


@main_bp.route('/')
def index():
    return jsonify({"message":"Bem vindo ao Crimson Claw Studio!"})
