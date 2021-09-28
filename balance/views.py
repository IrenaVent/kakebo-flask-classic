from balance import app
from flask import render_template, request, redirect, url_for, flash
from balance.models import DBManager
from balance.forms import MovimientoForm

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

    return render_template("inicio.html", items=movimientos) # items es solo el nombre de la variable

@app.route("/nuevo", methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientoForm()

    if request.method == "GET":
        # form es solo el nombre de la variable
        return render_template("nuevo_movimiento.html", form=formulario) 
    else:
        if formulario.validate():
            consulta = """ 
                    INSERT INTO movimientos (fecha, concepto, ingreso_gasto, cantidad) 
                    VALUES (:fecha, :concepto, :ingreso_gasto, :cantidad)
                """
            
            try:
                dbManager.modificaSQL(consulta, formulario.data)
            except Exception as e:
                print ("Se ha producido un error de acceso a base de datos", e)
                flash("Se ha producido un error en la base de datos")
                return render_template("nuevo_movimiento.html", form=formulario)

            return redirect(url_for("inicio"))
        else:
            return render_template("nuevo_movimiento.html", form=formulario)
       
       

# esta ruta es espécifica de flask, llama al registro y lo borra
@app.route("/borrar/<int:id>", methods=['GET', 'POST'])
def borrar(id):
    return f"Página de borrado de {id}"