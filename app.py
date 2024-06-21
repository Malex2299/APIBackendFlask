from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/contactos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

### Modelo de Contacto ###
class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False, unique=True)
    pais = db.Column(db.String(50), nullable=True)

    def __init__(self, nombre, apellido, telefono, pais=None):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.pais = pais

### Esquema de Marshmallow para Serialización ###
class EsquemaContacto(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contacto

esquema_contacto = EsquemaContacto()
esquemas_contactos = EsquemaContacto(many=True)

### Endpoints ###

# Obtener todos los contactos
@app.route('/contactos', methods=['GET'])
def obtener_contactos():
    todos_los_contactos = Contacto.query.all()
    resultado = esquemas_contactos.dump(todos_los_contactos)
    return jsonify(resultado), 200

# Paginación de contactos
@app.route('/contactos/paginados', methods=['GET'])
def obtener_contactos_paginados():
    pagina = request.args.get('pagina', 1, type=int)
    tamano_pagina = request.args.get('tamano_pagina', 10, type=int)
    contactos = Contacto.query.paginate(pagina, tamano_pagina, error_out=False)
    resultado = {
        'contactos': esquemas_contactos.dump(contactos.items),
        'tiene_siguiente': contactos.has_next,
        'tiene_anterior': contactos.has_prev,
        'num_siguiente': contactos.next_num if contactos.has_next else None,
        'num_anterior': contactos.prev_num if contactos.has_prev else None,
        'total_paginas': contactos.pages
    }
    return jsonify(resultado), 200

# Obtener un contacto por ID
@app.route('/contacto/<int:id>', methods=['GET'])
def obtener_contacto(id):
    contacto = Contacto.query.get(id)
    if contacto:
        return esquema_contacto.jsonify(contacto), 200
    else:
        return jsonify({'mensaje': 'Contacto no encontrado'}), 404

# Crear un nuevo contacto
@app.route('/contacto', methods=['POST'])
def crear_contacto():
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    telefono = request.json['telefono']
    pais = request.json.get('pais', None)
    
    nuevo_contacto = Contacto(nombre, apellido, telefono, pais)
    
    try:
        db.session.add(nuevo_contacto)
        db.session.commit()
        return esquema_contacto.jsonify(nuevo_contacto), 201
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'mensaje': 'Número de teléfono duplicado'}), 400

# Modificar un contacto existente
@app.route('/contacto/<int:id>', methods=['PUT'])
def actualizar_contacto(id):
    contacto = Contacto.query.get(id)
    if contacto:
        contacto.nombre = request.json['nombre']
        contacto.apellido = request.json['apellido']
        contacto.telefono = request.json['telefono']
        contacto.pais = request.json.get('pais', contacto.pais)
        
        db.session.commit()
        return esquema_contacto.jsonify(contacto), 200
    else:
        return jsonify({'mensaje': 'Contacto no encontrado'}), 404

# Eliminar un contacto
@app.route('/contacto/<int:id>', methods=['DELETE'])
def eliminar_contacto(id):
    contacto = Contacto.query.get(id)
    if contacto:
        db.session.delete(contacto)
        db.session.commit()
        return jsonify({'mensaje': 'Contacto eliminado'}), 200
    else:
        return jsonify({'mensaje': 'Contacto no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
