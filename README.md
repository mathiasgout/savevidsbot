# SaveVidsBot

## Version 1
- Frontend et backend liés grâce à `Flask` et ses templates
- Base de donnée NoSQL `Cloud Firestore`
- Utilisation de `NGINX` pour déployer le site
- Bot développé à l'aide du SDK python de l'API twitter : `tweepy`
- Le bot et le site sont conteneurisés dans des conteneurs `Docker`

### Fichiers à ajouter pour rendre le projet fonctionnel 

- `bot/.env`:
    - `TWITTER_API_KEY_PROD: str`
    - `TWITTER_API_KEY_SECRET_PROD: str`
    - `TWITTER_ACCESS_TOKEN_PROD: str`
    - `TWITTER_ACCESS_TOKEN_SECRET_PROD: str`
    - `TWITTER_API_KEY_DEV: str`
    - `TWITTER_API_KEY_SECRET_DEV: str`
    - `TWITTER_ACCESS_TOKEN_DEV: str`
    - `TWITTER_ACCESS_TOKEN_SECRET_DEV: str` 
- `bot/db/gcp_credentials.json`:
    - Clés d'un compte de service `GCP` qui à les droits d'écriture et lecture `Firebase`
