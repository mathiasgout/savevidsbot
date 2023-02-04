# SaveVidsBot

Projet arrêté car il n'y a plus de free tier de l'API twitter 

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
    - `SESSION_COOKIE_NAME: str`
    - `TWITTER_API_KEY_PROD: str`
    - `TWITTER_API_KEY_SECRET_PROD: str`
    - `TWITTER_ACCESS_TOKEN_PROD: str`
    - `TWITTER_ACCESS_TOKEN_SECRET_PROD: str`
    - `TWITTER_API_KEY_DEV: str`
    - `TWITTER_API_KEY_SECRET_DEV: str`
    - `TWITTER_ACCESS_TOKEN_DEV: str`
    - `TWITTER_ACCESS_TOKEN_SECRET_DEV: str`
- `website/flask_app/db/gcp_credentials.json`:
    - Clés d'un compte de service `GCP` qui à les droits d'écriture et lecture `Firebase`
- `website/nginx/ssl/certs/savevidsbot_com_chain.crt`
- `website/nginx/ssl/certs/server.key`
- `website/nginx/ssl/private/server.key`