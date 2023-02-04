# SaveVidsBot

## Version 2
- Mise en place d'un API avec `FastAPI` pour le backend.
- Migration vers une base de donnée SQL `postgreSQL` 
- Mise en place de tests avec `pytest` pour le backend et le bot
- Il manque la mise en place de `NGINX` pour le deploiement du backend
- Il manque le frontend, mais le projet est annulé car l'API twitter est maintenant payante

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