from flask import Flask


def create_app():
    app = Flask(__name__)
    

    from englix.views import englixBP
    app.register_blueprint(englixBP)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
