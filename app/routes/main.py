from flask import Blueprint,jsonify, request 
from app.models.usuario import LoginPayload
from pydantic import ValidationError
from bson import ObjectId



main_bp = Blueprint('main_bp',__name__)

#RF: O Sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route('/login',methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"error":e.errors()}),400
    except Exception as ex:
        return jsonify({"error":"Error durante a requisição do dado"}),500
    
    if user_data.username == 'admin' and user_data.password == '123':
        return jsonify({"message":"Login bem-sucedido"}),200
    else:
        return jsonify({"error":"Credenciais inválidas"}),401


#RF: O Sistema deve permitir listagem de todos os produtos
@main_bp.route('/produtos',methods=['GET'])
def get_produtos():
    return jsonify({"message":"Esta eh a rota dos produtos"})

#RF: O Sistema deve permitir a criação de um novo produto
@main_bp.route('/produtos',methods=['POST'])
def criar_produtos():
    return jsonify({"message":"Esta eh a rota de criação de produtos"})

#RF: O Sistema deve permitir a visualização dos detalhes de um produto
@main_bp.route('/produtos/<int:id_produto>',methods=['GET'])
def get_produto_por_id(id_produto):
    return jsonify({"message":f"Esta eh a rota do produto com id {id_produto}"})
#RF: O Sistema deve permitir a atualização de um unico produto e prod existente
@main_bp.route('/produtos/<int:id_produto>',methods=['PUT'])
def update_produto(id_produto):
    return jsonify({"message":"Esta eh a rota para atualizar o produto pelo id"})
#RF: O Sistema deve permitir a remoção de um unico produto e produto existente
@main_bp.route('/produtos/<int:id_produto>',methods=['DELETE'])
def remove_produto(id_produto):
    return jsonify({"message":"Esta eh a rota de remoção do produto pelo ID"})
#RF: O Sistema deve permitir a importação de vendas atraves de um arquivo
@main_bp.route('/vendas/upload',methods=['POST'])
def upload_vendas():
    return jsonify({'message':'essa eh a rota de upload de vendas'})


@main_bp.route('/')
def index():
    return jsonify({"message":"Bem vindo ao Crimson Claw Studio!"})



