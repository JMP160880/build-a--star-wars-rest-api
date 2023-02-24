"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User , Personaje , Planeta , Favorito
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ----------------------AQUI EMPIEZAN LOS ENDPOINTS -------------------------------
# OBTENEMOS TODOS LOS USUARIOS
@app.route('/user', methods=['GET'])
def handle_hello():

    users_query = User.query.all()
    results = list(map(lambda item: item.serialize(),users_query))

    response_body = {
        "msg": "ok",
        "results": results
    }
    return jsonify(response_body), 200

# OBTINER DATOS DE UN USUARIO
@app.route('/user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):

    user_query = User.query.filter_by(id=user_id).first()
  
    response_body = {
        "msg": "ok",
        "results": user_query.serialize()
    }
    return jsonify(response_body), 200

# OBTENER LISTA DE FAVORITOS DE UN USUARIO
# @app.route('/user/<int:user_id>/favorites', methods=['GET'])
# def get_info_user_favorites(user_id):

#     user_query = User.query.filter_by(id=user_id).first()
#     favorite_personaje_results = list(map(lambda item: item.serialize(),user_query))
  
#     response_body = {
#         "msg": "ok",
#         "favorite_results": user_query.serialize()
#     }
#     return jsonify(response_body), 200

# CREAR UN USUARIO EN EL CASO DE QUE NO ESTE EN LA DB
@app.route('/user', methods=['POST'])
def create_user():
    request_body=request.json
    user_query = User.query.filter_by(email=request_body["email"]).first()
    if user_query is None:

        user = User(email=request_body["email"], 
        password=request_body["password"])
        db.session.add(user)
        db.session.commit()
  
        response_body = {
            "msg": "El usuario ha sido creado con éxito",

        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Usuario ya existe"}), 400

# OBTENER TODOS LOS PERSONAJES
@app.route('/personaje', methods=['GET'])
def get_all_info_personajes():

    personajes_query = Personaje.query.all()
    results = list(map(lambda item: item.serialize(),personajes_query))

    response_body = {
        "msg": "ok",
        "results": results
    }
    return jsonify(response_body), 200

# OBTENER DATOS DE UN SOLO PERSONAJE
@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def get_info_personaje(personaje_id):

    personaje_query = Personaje.query.filter_by(id=personaje_id).first()
  
    response_body = {
        "msg": "ok",
        "results": personaje_query.serialize()
    }
    return jsonify(response_body), 200

# CREAR UN PERSONAJE EN EL CASO DE QUE NO ESTE EN LA DB
@app.route('/personaje', methods=['POST'])
def create_personaje():
    request_body=request.json
    personaje_query = Personaje.query.filter_by(name=request_body["name"]).first()
    if personaje_query is None:

        personaje = Personaje(name=request_body["name"])
        db.session.add(personaje)
        db.session.commit()
  
        response_body = {
            "msg": "El personaje ha sido creado con éxito",

        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Personaje ya existe"}), 400

# OBTENER TODOS LOS PLANETAS
@app.route('/planeta', methods=['GET'])
def get_all_info_planetas():

    planeta_query = Planeta.query.all()
    results = list(map(lambda item: item.serialize(),planeta_query))

    response_body = {
        "msg": "ok",
        "results": results
    }
    return jsonify(response_body), 200

# OBTENER DATOS DE UN SOLO PLANETA
@app.route('/planeta/<int:planeta_id>', methods=['GET'])
def get_info_planeta(planeta_id):

    planeta_query = Planeta.query.filter_by(id=planeta_id).first()
  
    response_body = {
        "msg": "ok",
        "results": planeta_query.serialize()
    }
    return jsonify(response_body), 200

# CREAR UN PLANETA EN EL CASO DE QUE NO ESTE EN LA DB
@app.route('/planeta', methods=['POST'])
def create_planeta():
    request_body=request.json
    planeta_query = Planeta.query.filter_by(name=request_body["name"]).first()
    if planeta_query is None:

        planeta = Planeta(name=request_body["name"])
        db.session.add(planeta)
        db.session.commit()
  
        response_body = {
            "msg": "El planeta ha sido creado con éxito",

        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Planeta ya existe"}), 400


# OBTENER TODOS LOS FAVORITOS
@app.route('/users/favorites', methods=['GET'])
def get_all_info_favoritos():

    favoritos_query = Favorito.query.all()
    results = list(map(lambda item: item.serialize(),favoritos_query))

    response_body = {
        "msg": "ok",
        "results": results
    }
    return jsonify(response_body), 200

# OBTENER UN FAVORITO
@app.route('/favorite', methods=['POST'])
def create_favorito():
    request_body=request.json
    # favorito_query = Favorito.query.filter_by(id=request_body["id"]).first()
    # if favorito_query is None:

    favorito = Favorito(planeta_id=request_body["planeta_id"],personaje_id=request_body["personaje_id"],usuario_id=request_body["usuario_id"])
    db.session.add(favorito)
    db.session.commit()
  
    response_body = {
            "msg": "El favorito ha sido creado con éxito",

        }

    return jsonify(response_body), 200
        # else:
        # return jsonify({"msg":"Este favorito ya existe"}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
