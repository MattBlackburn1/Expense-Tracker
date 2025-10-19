"""Application factory and core extensions.

Creates the Flask application via :func: create_app and initialises the
SQLAlchemy database instance. Registers feature blueprints (expenses, reports)
and ensures database tables are created on first run.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    """Create and configure the Flask application.

      Returns:
          Flask: Configured Flask application with database and blueprints
          registered. Uses a local SQLite file.
    """
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
    from .reports import bp as reports_bp
    app.register_blueprint(expenses_bp, url_prefix='/expenses')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    @app.route('/')
    def root():
        """Redirect bare root to the main expenses listing."""
        from flask import redirect, url_for
        return redirect(url_for('expenses.index'))

    return app