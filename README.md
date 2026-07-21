# CryptoSim Pro

Plateforme web de trading de cryptomonnaies (argent virtuel), avec prix live via CoinGecko.

## Stack
- Backend : Flask, Flask-SQLAlchemy, Flask-Login
- Frontend : HTML5, CSS3, JavaScript
- Base de données : SQLite

## Installation locale

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Créer un fichier `.env` à la racine avec :
```
SECRET_KEY=change-me
```

## Lancer le projet

```bash
python run.py
```

Le site est accessible sur http://127.0.0.1:5000


##test
