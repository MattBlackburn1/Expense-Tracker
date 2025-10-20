"""Local development entrypoint.

Runs the Flask development server using the application factory.
Use a production WSGI server (e.g. gunicorn) in deployment.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
