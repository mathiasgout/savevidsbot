from twitter_bot.bot import run_bot
from db.firebase_db import init_firebase_app
from config import DevConfig, ProdConfig

if __name__ == "__main__":
    init_firebase_app()
    run_bot(ProdConfig())
