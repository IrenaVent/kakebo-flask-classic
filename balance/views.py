from balance import app
from flask import render_template
from balance.models import DBManager

ruta_basedatos = app.config.get("DATABASEPATH")

# sólo vamos a utilizar una isntalcia de DBManager, se instancia cuando lanzamos run.py
dbManager = DBManager(ruta_basedatos) 

@app.route("/")
def inicio(): 

    consulta = """
        SELECT * 
          FROM movimientos 
         ORDER BY fecha;
    """
    movimientos = dbManager.consultaSQL(consulta)

    return render_template("inicio.html", items = movimientos)

@app.route("/nuevo", methods=['GET', 'POST'])
def nuevo():
    return "Página de alta de movimiento"

# esta ruta es espécifica de flask, llama al registro y lo borra
@app.route("/borrar/<int:id>", methods=['GET', 'POST'])
def borrar(id):
    return f"Página de borrado de {id}"