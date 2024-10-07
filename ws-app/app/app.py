from flask import Flask, request, jsonify, abort, send_from_directory
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from models import db, Votacion, Lista, Voto, Escanio
from dotenv import load_dotenv
import custom
import validations

#===ENV VARS = ===================
load_dotenv()

users = {
    "app": "Energia2025",
    "admin": "Juncal291"
}

app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./maestro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

with app.app_context():
    db.create_all()


# METODO DE AUTENTICACION DE REST API
@auth.verify_password
def verify_password(username, password):
    # SE PUEDE ENVIAR LUEGO A UNA DB
    if username in users and users[username] == password:
        return username
    return None

#================================================
# == VOTATION -  Methods
#================================================

#ENDPOINT TO ADD VOTATION
@app.route('/api/votacion/add', methods=['POST'])
@auth.login_required
def create_votacion():
    data = request.get_json()
    # Inputs Validations
    key_values =['summary','escanio_total']
    validations.validateKeyArgs(data, key_values)

    new_votacion = Votacion(summary=data['summary'], escanio_total=int(data['escanio_total']))
    db.session.add(new_votacion)
    db.session.commit()
    return jsonify({
        'message': 'Votacion created successfully',
        'idVotacion': new_votacion.idVotacion,
        'created_at': new_votacion.created_at,
        'status': new_votacion.status,
        'summary': new_votacion.summary,
        'escanio_total': new_votacion.escanio_total,
    }), 201

#ENDPOINT TO LIST  ALL VOTACION
@app.route('/api/votacion/list', methods=['GET'])
@auth.login_required
def list_votacion():
    qry = Votacion.query

    if 'idVotacion' in  request.args:
        idVotacion = request.args.get('idVotacion')
        votacion = qry.get(idVotacion)
        if not votacion:
            return jsonify({"error": "Votacion with id {} does not exist".format(idVotacion)}), 400
        
        return jsonify({'idVotacion': votacion.idVotacion, 
                        'created_at': votacion.created_at, 
                        'status': votacion.status, 
                        'summary': votacion.summary,
                        'escanio_total': votacion.escanio_total
                        }),200
    else:
        # FILTRO OPCIONAL POR STATUS
        if 'status' in request.args:
            status = request.args.get('status')
            qry = qry.filter(Votacion.status.like(f'%{status}%'))

        votaciones = qry.all()
        
        return jsonify([{'idVotacion': votacion.idVotacion, 
                        'created_at': votacion.created_at, 
                        'status': votacion.status, 
                        'summary': votacion.summary,
                        'escanio_total': votacion.escanio_total
                        } for votacion in votaciones]),200

#ENDPOINT TO BORRADO LOGICO DE VOTACION
@app.route('/api/votacion/del', methods=['POST'])
@auth.login_required
def del_votacion():
    data = request.get_json()
    
    # Inputs Validations
    key_values =['idVotacion']
    validations.validateKeyArgs(data, key_values)

    votacion = Votacion.query.get(data['idVotacion'])
    if not votacion:
        return jsonify({"error": "Votacion with id {} does not exist".format(data['idVotacion'])}), 400
    else:
        votacion.deleted = 't'
        db.session.commit()
        return jsonify({'message': 'Votacion deleted successfully'}),200

#ENDPOINT TO CALCULATE ESCAÑO
@app.route('/api/votacion/calcular', methods=['POST'])
@auth.login_required
def calculate_escanio():
    partidos_votos = []
    escanios_total = 0
    division_votos = []
    data = request.get_json()
    
    # Inputs Validations
    key_values =['idVotacion']
    validations.validateKeyArgs(data, key_values)

    votacion = Votacion.query.get(data['idVotacion'])
    if not votacion:
        return jsonify({"error": "Votacion with id {} does not exist".format(data['idVotacion'])}), 400
    else:
        escanios_total = votacion.escanio_total

    listas = Lista.query.filter(Lista.idVotacion == data['idVotacion']).all()


    if not listas:
        return jsonify({"error": "La Votacion with id {} dont have Listas".format(data['idVotacion'])}), 400

    try:
        #Armo una lista con el ID de partido y la CANTIDAD de votos obtenidos
        for lista in listas:
            partidos_votos.append((lista.idLista, lista.votos_total))

        # - Armo un Diccionario para luego almacenar con el ID de Partido y los Escanios obtenidos
        escanios_partidos = {partido: 0 for partido, votos in partidos_votos}

        # - Recorro los partidos y sus votos y realizo la lista con la division de los votos
        # para luego obtener los N mayores en base a la cantidad de escanios totales.
        for partido, votos in partidos_votos:
            for i in range(1, escanios_total + 1):
                division_votos.append((partido, votos / i))

        # - Orderno por cantidad de Votos Descendentes utilizando como campo clave 
        # la cantidad de votos que es el primer elemento del cada registro de DIVISION de VOTOS
        division_votos.sort(key=lambda x: x[1], reverse=True)

        # - Obtengo lo primeros N elementos  de la lista de division de votos
        # y lo sumariso al partido correspondiente en el diccionario de escanios
        for i in range(escanios_total):
            partido = division_votos[i][0]
            escanios_partidos[partido] += 1

        for partido in escanios_partidos:
            print(partido)
            print(escanios_partidos[partido])
            lista = Lista.query.get(partido)
            lista.escanios_total = escanios_partidos[partido]
            lista.status = 'closed'
            new_escanio = Escanio(idLista=int(partido), escanios_asignado=escanios_partidos[partido])
            db.session.add(new_escanio)
            db.session.commit()
        votacion.status = 'closed'
        db.session.commit()
        
        return jsonify({"success": "Se calcularon correctamente los escanios"}), 200
    except:
        return jsonify({"error": "Error al calcular los escanios"}), 400

#================================================
# == LISTAS -  Methods
#================================================
#ENDPOINT TO ADD LISTAS
@app.route('/api/listas/add', methods=['POST'])
@auth.login_required
def create_lista():
    data = request.get_json()
    # Inputs Validations
    key_values =['idVotacion','summary','description']
    validations.validateKeyArgs(data, key_values)

    # ===Exist Votacion Validation
    votacion = Votacion.query.get(data['idVotacion'])
    if not votacion:
        return jsonify({"error": "Votacion with id {} does not exist".format(data['idVotacion'])}), 400

    new_lista = Lista(idVotacion=data['idVotacion'], summary=data['summary'], description=data['description'])
    db.session.add(new_lista)
    db.session.commit()

    return jsonify({
        'message': 'Lista created successfully',
        'idLista': new_lista.idLista,
        'idVotacion':  new_lista.idVotacion,
        'created_at': new_lista.created_at,
        'created_by':  new_lista.created_by,
        'summary': new_lista.summary,
        'description': new_lista.description,
        'votos_total':  new_lista.votos_total,
        }), 201

#ENDPOINT TO GET LISTAS
@app.route('/api/listas/list', methods=['GET'])
@auth.login_required
def list_listas():
    qry = Lista.query

        # FILTRO OPCIONAL POR STATUS
    if 'idLista' in request.args:
        idLista = request.args.get('idLista')
        lista = Lista.query.get(idLista)
        if not lista:
            return jsonify({"error": "Lista with id {} does not exist".format(idLista)}),400
        return jsonify({'idLista': lista.idLista,
                     'idVotacion': lista.idVotacion,
                     'created_at': lista.created_at,
                     'created_by': lista.created_by,
                     'summary': lista.summary,
                     'status': lista.status,
                     'description': lista.description,
                     'votos_total': lista.votos_total,
                     'escanios_total': lista.escanios_total
                     }), 200
    else:

        # FILTRO OPCIONAL POR Votacion
        if 'idVotacion' in request.args:
            idVotacion = request.args.get('idVotacion')
            qry = qry.filter(Lista.idVotacion == idVotacion)
        
        listas = qry.all()
    
    return jsonify([{'idLista': lista.idLista,
                     'idVotacion': lista.idVotacion,
                     'created_at': lista.created_at,
                     'created_by': lista.created_by,
                     'summary': lista.summary,
                     'description': lista.description,
                     'votos_total': lista.votos_total,
                     'escanios_total': lista.escanios_total
                     } for lista in listas]), 200

#================================================
# == Votos -  Methods
#================================================
#ENDPOINT TO REGISTRY VOTO
@app.route('/api/votos/set', methods=['POST'])
@auth.login_required
def reg_votos():
    data = request.get_json()
    
    # Inputs Validations
    key_values =['idLista','votos_cant']
    validations.validateKeyArgs(data, key_values)

    # ===Exist Lista Validation
    lista = Lista.query.get(data['idLista'])
    if not lista:
        return jsonify({"error": "Lista with id {} does not exist".format(data['idLista'])}), 400

    new_voto = Voto(idLista=data['idLista'], votos_cant=data['votos_cant'])
    db.session.add(new_voto)
    lista.votos_total = data['votos_cant']
    db.session.commit()
    
    return jsonify({'message': 'Voto set successfully',
                    'idVoto': new_voto.idVoto,
                    'idLista': new_voto.idLista,
                    'created_at': new_voto.created_at,
                    'created_by': new_voto.created_by,
                    'votos_cant': new_voto.votos_cant}), 201

#ENDPOINT TO ADD VOTO
@app.route('/api/votos/add', methods=['POST'])
@auth.login_required
def add_voto():
    data = request.get_json()
    
    # Inputs Validations
    key_values =['idLista']
    validations.validateKeyArgs(data, key_values)

    # ===Exist Lista Validation
    lista = Lista.query.get(data['idLista'])
    if not lista:
        return jsonify({"error": "Lista with id {} does not exist".format(data['idLista'])}), 400

    lista.votos_total += 1
    db.session.commit()
    
    return jsonify({'message': 'Voto added successfully'}), 201

#ENDPOINT TO history Votos
@app.route('/api/votos/historico', methods=['GET'])
@auth.login_required
def historico_votos():
    qry = Voto.query
    if 'idLista' in request.args:
            idLista = request.args.get('idLista')
            qry = qry.filter(Voto.idLista == idLista)

    votos = qry.all()
    return jsonify([{'idVoto': voto.idVoto,
                     'idLista': voto.idLista,
                     'created_at': voto.created_at,
                     'created_by': voto.created_by,
                     'votos_cant': voto.votos_cant} for voto in votos
                     ]), 200


# = Init APP = 
if __name__ == '__main__':
    app.run(debug=True,port=5006)
