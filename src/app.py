from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL
# Se usara con datos JSON (JavaScript Objtect Notation)

app = Flask(__name__)

conexion = MySQL(app)


@app.route('/cursos', methods=['GET'])
def listat_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo,nombre, creditos FROM curso"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []
        for fila in datos:
            curso = {'codigo': fila[0], 'nombre': fila[1], 'creditos': fila[2]}
            cursos.append(curso)
        return jsonify({'cursos': cursos, 'Mensaje': "Cursos Listados"})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})


@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM curso WHERE codigo = '{0}'".format(
            codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {'codigo': datos[0],
                     'nombre': datos[1], 'creditos': datos[2]}
            return jsonify({'curso': curso, 'Mensaje': "Cursos encontrado"})
        else:
            return jsonify({'Mensaje': "Cursos no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})


def page_not_for(error):
    return "<h1>Esta pagina que ingresa es erronea ... :(</h1>", 404


@app.route('/cursos', methods=['POST'])
def registrar_curso():
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO curso (codigo,nombre,creditos) 
        VALUES ('{0}','{1}',{2})""".format(request.json['codigo'], request.json['nombre'], request.json['creditos'])
        cursor.execute(sql)
        conexion.connection.commit()  # confirma la accion de insercion
        return jsonify({'mensaje': 'Curso registrado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})


@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM curso WHERE codigo = '{0}'". format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()  # confirma la accion de insercion
        return jsonify({'mensaje': 'Curso Eliminado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})


@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = """UPDATE curso SET nombre = '{0}' , creditos= {1} WHERE codigo = '{2}' 
        """.format(request.json['nombre'], request.json['creditos'], codigo)
        cursor.execute(sql)
        conexion.connection.commit()  # confirma la accion de insercion
        return jsonify({'mensaje': 'Curso actualizado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_for)
    app.run()
