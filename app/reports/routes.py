from datetime import date
from flask import request, request_started, render_template
from sqlalchemy import select, func
from . import bp
from .. import db

def month_key(dt: date) -> str:
    """Return a YYYY-MM formatted string for the given date."""
    return f"{dt.month:02d}"

@bp.get("/")
def index():
    """
    Generate expense reports showing the last six months of totals
    and per-category breakdowns for a selected month.
    """
    from ..models import Expense

    rows = db.session.execute(
        select(func.strftime("%Y-%m", Expense.date).label("ym"),
               func.sum(Expense.amount))
        .group_by("ym")
    ).all()

    month_totals = sorted(rows, key=lambda r: r[0], reverse=True)[:6]
    month_totals = list(sorted(month_totals, key=lambda r: r[0]))

    selected_month = request.args.get("month") or month_key(date.today())

    by_cat = db.session.execute(
        select(Expense.category, func.sum(Expense.amount))
        .where(func.strftime("%Y-%m", Expense.date) == selected_month)
        .group_by(Expense.category)
    ).all()

    return render_template(
        "reports/index.html",
        month_totals=month_totals,
        selected_month=selected_month,
        by_cat=by_cat
    )