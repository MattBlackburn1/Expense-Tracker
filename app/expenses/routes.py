"""Expenses feature: list, filter, create, and delete expense records."""

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func, select
from datetime import date
from . import bp
from .. import db
from ..models import Expense
from ..forms import ExpenseForm, CATEGORIES

def month_key(dt: date) -> str:
    """Return YYYY-MM string for a given date.

      Args:
          dt: A date object.

      Returns:
          str: Month key in the form 'YYYY-MM'.
      """
    return f"{dt.month:02d}"

@bp.get("/")
def index():
    """List expenses with optional month/category filters and show summaries.

    Query params:
        month (YYYY-MM): Filter expenses to a specific month. Defaults to current.
        cat (str): Category filter ('All' shows every category).

    Template:
        Renders 'expenses/index.html' with:
            items (list[Expense]): Filtered expense rows.
            month (str): Selected YYYY-MM.
            month_total (float): Sum of amounts for the selected month.
            by_cat (list[tuple[str, float]]): Totals grouped by category.
            categories (list[str]): Available categories incl. 'All'.
            selected_cat (str): Current category filter.
    """
    q_month = request.args.get("month") or month_key(date.today())
    q_cat = request.args.get("cat", "All")

    base = select(Expense).where(func.strftime("%Y-%m", Expense.date) == q_month)
    if q_cat != "All":
        base = base.where(Expense.category == q_cat)

    items = (db.session.execute(base.order_by(Expense.date.desc())).scalars().all())

    month_total = db.session.execute(
        select(func.sum(Expense.amount)).where(
            func.strftime("%Y-%m", Expense.date) == q_month
        )
    ).scalar() or 0.0

    by_cat = db.session.execute(
        select(Expense.category, func.sum(Expense.amount))
        .where(func.strftime("%Y-%m", Expense.date) == q_month)
        .group_by(Expense.category)
    ).all()

    return render_template(
        "expenses/index.html",
        items=items,
        month=q_month,
        month_total=month_total,
        by_cat=by_cat,
        categories=["All"] + CATEGORIES,
        selected_cat=q_cat
    )

@bp.route("/add", methods=("GET", "POST"))
def add():
    """Create a new expense via form submit.

    GET: Render the form.
    POST: Validate and persist a new :class:`Expense`, then redirect to list.
    """
    form = ExpenseForm()
    if form.validate_on_submit():
        e = Expense(
            date=form.date.data,
            amount=float(form.amount.data),
            category=form.category.data,
            note=form.note.data or "",
        )
        db.session.add(e)
        db.session.commit()
        flash("Expense added", "Success")
        return redirect(url_for("expenses.index"))
    return render_template(
        "expenses/add.html", form=form)

@bp.post("/delete/<int:id>")
def delete(id):
    """Delete a single expense by primary key.

    Args:
        id: Expense.id to delete.
    """
    def delete():
        e = Expense.query.get_or_404(id)
        db.session.delete(e)
        db.session.commit()
        flash("Deleted", "info")
        return redirect(url_for("expenses.index"))