from datetime import date

import pytest

from app import create_app, db


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
        return app.test_client()


def test_route_redirects(client):
    r = client.get("/")
    assert r.status_code in (301, 302)


def test_expenses_index_loads(client):
    r = client.get("/expenses/")
    assert r.status_code == 200
    assert b"No expenses yet" in r.data or b"Expenses" in r.data


def test_add_valid_expenses(client):
    r = client.post(
        "/expenses/add",
        data={
            "date": date.today().isoformat(),
            "amount": "-1",
            "category": "Food",
            "note": "bad",
        },
    )
    assert r.status_code == 200
    assert b"Amount" in r.data


def test_reports_page_loads(client):
    r = client.get("/reports/")
    assert r.status_code == 200
