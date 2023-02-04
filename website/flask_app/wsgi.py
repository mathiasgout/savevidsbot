from app import create_app
from db.firebase_db import init_firebase_app


app = create_app(config="ProdConfig")
init_firebase_app()

if __name__ == "__main__":
    app.run()
