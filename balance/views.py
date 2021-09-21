from balance import app
from flask import render_template


@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/nuevo", methods=['GET', 'POST'])
def nuevo():
    return "Página de alta de movimiento"

#esta ruta es espécifica de flask, llama al registro y lo borra
@app.route("/borrar/<int:id>", methods=['GET', 'POST'])
def borrar(id):
    return f"Página de borrado de {id}"