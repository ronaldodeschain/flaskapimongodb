from flask import Blueprint,jsonify

categoria_bp = Blueprint('categoria_bp',__name__,url_prefix='/categorias')

@categoria_bp.route('/',methods=['GET'])
def get_categorias():
    return jsonify({"message":"Retorna a lista de todas as categorias."})

@categoria_bp.route('/',methods=['POST'])
def create_categoria():
    return jsonify({"message":"Cria uma nova categoria."})