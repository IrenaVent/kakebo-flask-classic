from balance import app
from flask import render_template, request, redirect, url_for, flash
from balance.models import DBManager
from balance.forms import MovimientoForm
from datetime import date

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
    if request.method == "GET":

        consulta = """
        SELECT id, fecha, concepto, ingreso_gasto, cantidad 
          FROM movimientos
        WHERE id = ?;
    """
        movimientos = dbManager.consultaSQL(consulta,[id])
        if len(movimientos) == 0:
            flash(f"Movimiento {id} no encontrado")
            # para cambiar de ruta usam redirect
            return redirect(url_for("inicio"))

        el_movimiento = movimientos[0]
        # la fecha del movimiento no es adecuado, esto debe pasar a models / no se debe hacer aquí
        el_movimiento["fecha"] = date.fromisoformat(el_movimiento["fecha"])
        formulario = MovimientoForm(data = el_movimiento)

        # pasamos id para pasar la id a la ruta cd action = "/borrar" en le html
        return render_template("borrar_movimiento.html", form=formulario, id=el_movimiento["id"])

    else: 
        consulta = """
        DELETE FROM movimientos WHERE id = ?;
    """
        try:
            dbManager.modificaSQL(consulta, [id])
        except Exception as e:
            print ("Se ha producido un error de acceso a base de datos", e)
            flash("Se ha producido un error en la base de datos")        
            return redirect(url_for("inicio"))
        return redirect(url_for("inicio"))

@app.route("/modificar/<int:id>", methods=['GET', 'POST'])
def modificar(id):
    formulario = MovimientoForm()

    if request.method == "GET":

        consulta = """
        SELECT id, fecha, concepto, ingreso_gasto, cantidad 
          FROM movimientos
        WHERE id = ?;
    """
        try:
            movimientos = dbManager.consultaSQL(consulta,[id])
        except Exception as e:
            print ("Se ha producido un error de acceso a base de datos", e)
            flash("Se ha producido un error en la base de datos")
            return render_template("nuevo_movimiento.html", form=formulario)
        
        if len(movimientos) == 0:
            flash(f"Movimiento {id} no encontrado")
            return redirect(url_for("inicio"))

        el_movimiento = movimientos[0]
        el_movimiento["fecha"] = date.fromisoformat(el_movimiento["fecha"])
        formulario = MovimientoForm(data = el_movimiento)

        return render_template("modificar_movimiento.html", form=formulario, id=el_movimiento["id"])
    else: 
        consulta = """
        UPDATE movimientos SET fecha = :fecha, concepto = :concepto, ingreso_gasto = :ingreso_gasto WHERE id = :id;
    """
        try:
            movimiento = dbManager.modificaSQL(consulta, formulario.data)
        except Exception as e:
            print ("Se ha producido un error de acceso a base de datos", e)
            flash("Se ha producido un error en la base de datos")        
            return redirect(url_for("inicio"))
        return redirect(url_for("inicio"))