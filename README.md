# SaveVidsBot
https://twitter.com/savevidsbot

Projet arrêté à cause des changements de l'API twitter.

**LE DEVELOPPEMENT DE CETTE VERSION N'EST PAS TERMINÉ, VOIR BRANCHE `v1` POUR UNE VERSION FINALISÉE** 

## Version 2
- Mise en place d'un API avec `FastAPI` pour le backend.
- Migration vers une base de donnée SQL `postgreSQL` 
- Mise en place de tests avec `pytest` pour le backend et le bot
- Il manque la mise en place de `NGINX` pour le deploiement du backend (voir branche `v1`)
- Le frontend n'est pas terminé (voir branche `v1` pour un frontend à base de template `Flask`)

### Fichiers à ajouter pour rendre le projet fonctionnel

#### Bot
- `bot/bot/.env`:
    - `ADMIN_USERNAME=<ADMIN USERNAME>`
    - `ADMIN_PASSWORD:<ADMIN PASSWORD>`
    - `URL_PREFIX=<URL PREFIX>` 
    - `API_PREFIX=<API PREFIX>`
    - `TRACK=<@ TO TRACK>`
    - `TWITTER_API_KEY=<TWITTER API KEY>`    
    - `TWITTER_API_KEY_SECRET=<TWITTER API KEY SECRET>`
    - `TWITTER_ACCESS_TOKEN=<TWITTER ACCESS TOKEN>`
    - `TWITTER_ACCESS_TOKEN_SECRET=<TWITTER ACCESS TOKEN SECRET>`

#### Backend
- `backend/app/.env`:
    - `SECRET_KEY=<APP SECRET KEY>`
    - `TWITTER_API_KEY=<TWITTER API KEY>`    
    - `TWITTER_API_KEY_SECRET=<TWITTER API KEY SECRET>`
    - `TWITTER_ACCESS_TOKEN=<TWITTER ACCESS TOKEN>`
    - `TWITTER_ACCESS_TOKEN_SECRET=<TWITTER ACCESS TOKEN SECRET>`
- `backend/app/database.ini`:
    - Fichier `.ini` avec une section nommée `[postgresql]`
    - La section `[postgresql]` a comme paramètres:
        - `host=<HOST>`
        - `port=<PORT>`
        - `database=<DB NAME>`
        - `user=<USER NAME>`
        - `password=<USER PASSWORD>`
