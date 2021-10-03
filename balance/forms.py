from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
import datetime 


        # incluir dentro de campo fecha []
def validar_fecha(formulario, campo):
    hoy = datetime.date.today()
    if campo.data > hoy:
        raise ValidationError("La fecha no puede ser posterior a hoy - soy externo") 

class MovimientoForm(FlaskForm):

    fecha = DateField("Fecha", validators=[DataRequired(message="Debe informar la fecha"), validar_fecha]) #indicando la instancia de un validator
    # si se pone así el validar_fecha, es porque la función de validar está fuera de la clase
    concepto = StringField("Concepto", validators=[DataRequired(message="Debe informar el concepto"), Length(min=10)])
    ingreso_gasto = RadioField(validators=[DataRequired(message="Debe informar el tipo de movimiento")], choices=[("G", "Gasto"), ("I", "Ingreso")])
    cantidad = FloatField("Cantidad", validators=[DataRequired(message="Debe informar la cantidad"), NumberRange(message="Debe ser un importe positivo", min =0.01)])

    submit = SubmitField("Aceptar")

    # # otra manera de hacer un ValueError propio 
    # def validate_fecha(self, campo): 
    #     hoy = datetime.data.today()
    #     if campo.data > hoy:
    #         raise ValidationError("La fecha no puede ser posterior a hoy - soy interno")