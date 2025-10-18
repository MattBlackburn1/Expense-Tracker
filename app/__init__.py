from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite:///expenses.sqlite3',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY='dev',
    )

    db.init_app(app)

    from .models import Expense
    with app.app_context():
        db.create_all()

    from .expenses import bp as expenses_bp
    app.register_blueprint(expenses_bp, url_prefix='/expenses')

    @app.route('/')
    def root():
        from flask import redirect, url_for
        return redirect(url_for('expenses.index'))

    return app