from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class MovimientoForm(FlaskForm):
    fecha = DateField("Fecha", validators=[DataRequired(message="Debe informar la fecha")]) #indicando la instancia de un validator
    concepto = StringField("Concepto", validators=[DataRequired(message="Debe informar el concepto"), Length(min=10)])
    ingreso_gasto = RadioField(validators=[DataRequired(message="Debe informar el tipo de movimiento")], choices=[("G", "Gasto"), ("I", "Ingreso")])
    cantidad = FloatField("Cantidad", validators=[DataRequired(message="Debe informar la cantidad"), NumberRange(message="Debe ser un importe positivo", min =0.01)])

    submit = SubmitField("Aceptar")
