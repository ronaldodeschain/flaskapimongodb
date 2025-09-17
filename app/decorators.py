from functools import wraps
from flask import request,jsonify,current_app, g
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if not auth_header.startswith('Bearer '):
                return jsonify({'message': 'Token mal formado, "Bearer " prefix ausente'}), 400
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'message':'Token mal formado'}), 400

        if not token:
            return jsonify({'message':'Token não encontrado'}),401
        
        try:
            # O parâmetro correto é 'algorithms' (plural).
            data = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error':'Token expirado'}),401
        except jwt.InvalidTokenError:
            return jsonify({'error':'Token invalido'}),401

        # Armazena o payload do token no objeto 'g' do Flask, que é seguro para threads e específico para cada requisição.
        g.user = data
        return f(*args,**kwargs)
        
    return decorated