"""Database models used by the application."""

from datetime import date

from . import db


class Expense(db.Model):
    """A single expense record.

    Columns:
        id (int): Primary key.
        date (date): When the expense occurred. Defaults to today.
        amount (float): Positive currency amount.
        category (str): High-level category label (e.g., 'Food').
        note (str|None): Optional free-text description (≤ 200 chars).
    """

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(200))
