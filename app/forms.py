from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length

CATEGORIES = ["Food", "Transport", "Bills", "Entertainment", "Other"]

class ExpenseForm(FlaskForm):
    date = DateField(validators=[DataRequired()])
    amount = DecimalField("Amount", places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    category = SelectField("Category", choices=[(c, c) for c in CATEGORIES], validators=[DataRequired()])
    note = StringField("Note", validators=[Length(max=200)])
    submit = SubmitField("Save")