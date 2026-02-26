import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect
from dao.producto_dao import ProductoDAO
from dto.producto_dto import ProductoDTO

app = Flask(__name__)
@app.route("/")
def inicio():
    return redirect("/productos")

@app.route("/productos")
def productos():
    lista = ProductoDAO.listar()
    return render_template("productos.html", productos=lista)

@app.route("/nuevo")
def nuevo():
    return render_template("formulario.html")

@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    archivo = request.files["imagen"]
    nombre_imagen = None

    if archivo and archivo.filename != "":
        nombre_imagen = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen))

    producto = ProductoDTO(None, nombre, descripcion, precio, stock, nombre_imagen)
    ProductoDAO.guardar(producto)

    return redirect("/productos")

@app.route("/editar/<int:id>")
def editar(id):
    producto = ProductoDAO.obtener_por_id(id)
    return render_template("formulario.html", producto=producto)

@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    archivo = request.files["imagen"]
    producto_actual = ProductoDAO.obtener_por_id(id)
    nombre_imagen = producto_actual.imagen

    if archivo and archivo.filename != "":
        nombre_imagen = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen))

    producto = ProductoDTO(id, nombre, descripcion, precio, stock, nombre_imagen)
    ProductoDAO.actualizar(producto)

    return redirect("/productos")

@app.route("/eliminar/<int:id>")
def eliminar(id):
    ProductoDAO.eliminar(id)
    return redirect("/productos")

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == "__main__":
    app.run(debug=True)