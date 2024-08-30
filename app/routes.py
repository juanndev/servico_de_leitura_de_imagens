from flask import request, jsonify
from app import app, db
from app.models import Measure
import base64
import requests

# Função auxiliar para verificar se a leitura já existe
def reading_exists(customer_code, measure_type, measure_datetime):
    return db.session.query(Measure).filter_by(
        customer_code=customer_code,
        measure_type=measure_type,
        measure_datetime=measure_datetime
    ).first() is not None

# Função auxiliar para validar o Base64
def is_base64_encoded(data):
    try:
        base64.b64decode(data, validate=True)
        return True
    except Exception:
        return False

@app.route('/')
def index():
    return "Bem-vindo ao serviço de medição!"

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()

    # Validação dos dados recebidos
    if not data or 'image' not in data or 'customer_code' not in data or 'measure_datetime' not in data or 'measure_type' not in data:
        return jsonify({
            "error_code": "INVALID_DATA",
            "error_description": "Dados fornecidos são inválidos"
        }), 400

    image = data['image']
    customer_code = data['customer_code']
    measure_datetime = data['measure_datetime']
    measure_type = data['measure_type'].upper()

    if not is_base64_encoded(image):
        return jsonify({
            "error_code": "INVALID_DATA",
            "error_description": "O campo 'image' não está codificado em Base64"
        }), 400

    if measure_type not in ["WATER", "GAS"]:
        return jsonify({
            "error_code": "INVALID_TYPE",
            "error_description": "Tipo de medição não permitido"
        }), 400

    if reading_exists(customer_code, measure_type, measure_datetime):
        return jsonify({
            "error_code": "DOUBLE_REPORT",
            "error_description": "Leitura do mês já realizada"
        }), 409

    # Integração com a API de LLM para extrair o valor da imagem
    llm_api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"  # Substitua pela URL real da API
    api_key = "AIzaSyDVymRTnP_EmDVzPKVDx3CqXu10GgN234Y"  # Substitua pela sua chave de API real

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(llm_api_url, json={
        'image': image
    }, headers=headers)

    if response.status_code != 200:
        return jsonify({
            "error_code": "LLM_ERROR",
            "error_description": "Erro ao consultar a API de LLM"
        }), 500

    result = response.json()
    image_url = result.get('image_url')
    measure_uuid = result.get('measure_uuid')
    measure_value = result.get('measure_value')

    # Salvar no banco de dados
    new_measure = Measure(
        customer_code=customer_code,
        measure_datetime=measure_datetime,
        measure_type=measure_type,
        measure_value=measure_value,
        image_url=image_url,
        measure_uuid=measure_uuid
    )
    db.session.add(new_measure)
    db.session.commit()

    return jsonify({
        "image_url": image_url,
        "measure_value": measure_value,
        "measure_uuid": measure_uuid
    }), 200

@app.route('/confirm', methods=['PATCH'])
def confirm():
    data = request.get_json()

    # Validação dos dados recebidos
    if not data or 'measure_uuid' not in data or 'confirmed_value' not in data:
        return jsonify({
            "error_code": "INVALID_DATA",
            "error_description": "Dados fornecidos são inválidos"
        }), 400

    measure_uuid = data['measure_uuid']
    confirmed_value = data['confirmed_value']

    # Verificar se a leitura existe
    measure = db.session.query(Measure).filter_by(measure_uuid=measure_uuid).first()
    if not measure:
        return jsonify({
            "error_code": "MEASURE_NOT_FOUND",
            "error_description": "Leitura não encontrada"
        }), 404

    if measure.has_confirmed:
        return jsonify({
            "error_code": "CONFIRMATION_DUPLICATE",
            "error_description": "Leitura já confirmada"
        }), 409

    # Atualizar o valor confirmado no banco de dados
    measure.measure_value = confirmed_value
    measure.has_confirmed = True
    db.session.commit()

    return jsonify({
        "success": True
    }), 200

@app.route('/<customer_code>/list', methods=['GET'])
def list_measures(customer_code):
    measure_type = request.args.get('measure_type', '').upper()

    if measure_type not in ["", "WATER", "GAS"]:
        return jsonify({
            "error_code": "INVALID_TYPE",
            "error_description": "Tipo de medição não permitido"
        }), 400

    measures = db.session.query(Measure).filter_by(customer_code=customer_code)
    if measure_type:
        measures = measures.filter_by(measure_type=measure_type)

    measures = measures.all()
    if not measures:
        return jsonify({
            "error_code": "MEASURES_NOT_FOUND",
            "error_description": "Nenhuma leitura encontrada"
        }), 404

    result = []
    for measure in measures:
        result.append({
            "measure_uuid": measure.measure_uuid,
            "measure_datetime": measure.measure_datetime.isoformat(),
            "measure_type": measure.measure_type,
            "has_confirmed": measure.has_confirmed,
            "image_url": measure.image_url
        })

    return jsonify({
        "customer_code": customer_code,
        "measures": result
    }), 200
