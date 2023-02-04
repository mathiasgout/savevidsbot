# SaveVidsBot

Projet arrêté car il n'y a plus de free tier

## Version 2
- Mise en place d'un API avec `FastAPI` pour le backend.
- Migration vers une base de donnée SQL `postgreSQL` 
- Mise en place de tests avec `pytest` pour le backend et le bot
- Il manque la mise en place de `NGINX` pour le deploiement du backend (voir branche `v1`)
- Il manque le frontend (voir branche `v1` pour un frontend à base de template `Flask`)

### Fichiers à ajouter pour rendre le projet fonctionnel

#### Bot
- `bot/bot/.env`:
    - `URL_PREFIX: str`
    - `API_PREFIX: str`
    - `TRACK: str`
    - `TWITTER_API_KEY: str`    
    - `TWITTER_API_KEY_SECRET: str`
    - `TWITTER_ACCESS_TOKEN: str`
    - `TWITTER_ACCESS_TOKEN_SECRET: str`

#### Backend
- `backend/app/.env`:
    - `SECRET_KEY: str`
    - `TWITTER_API_KEY: str`    
    - `TWITTER_API_KEY_SECRET: str`
    - `TWITTER_ACCESS_TOKEN: str`
    - `TWITTER_ACCESS_TOKEN_SECRET: str`
- `backend/app/database.ini`:
    - Fichier `.ini` avec une section nommée `[postgresql]`
    - Paramètres dans la section `[postgresql]`:
        - `host: str`
        - `port: int`
        - `database: str`
        - `user: str`
        - `password: str`