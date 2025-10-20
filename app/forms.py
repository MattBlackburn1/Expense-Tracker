"""WTForms definitions and validation rules for user input."""

from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

CATEGORIES = ["Food", "Transport", "Bills", "Entertainment", "Other"]


class ExpenseForm(FlaskForm):
    """Form for creating a :class:`Expense`.

    Fields:
        date: Required; the expense date.
        amount: Required; positive decimal with 2dp.
        category: Required; one of :data:`CATEGORIES`.
        note: Optional; ≤ 200 characters.
    """

    date = DateField(validators=[DataRequired()])
    amount = DecimalField(
        "Amount", places=2, validators=[DataRequired(), NumberRange(min=0.01)]
    )
    category = SelectField(
        "Category", choices=[(c, c) for c in CATEGORIES], validators=[DataRequired()]
    )
    note = StringField("Note", validators=[Length(max=200)])
    submit = SubmitField("Save")
