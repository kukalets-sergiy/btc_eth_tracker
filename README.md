# BTC / ETH Tracker  
FastAPI + Django ORM + Django Admin (mounted inside FastAPI)

The application stores and exposes latest BTC and ETH data.

- **BTC provider:** Blockstream  
- **ETH provider:** Blockchair  
- **Stats:** CoinMarketCap (free tier does not provide block number)

---

## Requirements

- Python 3.10+
- Poetry
- Docker + Docker Compose

---

## Run

```bash
git clone https://github.com/kukalets-sergiy/btc_eth_tracker.git
cd btc_eth_tracker
cp fastapi/fastapi.env.tmpl fastapi/fastapi.env
```
Local Development (without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
poetry install
chmod +x scripts/lock.sh
bash scripts/lock.sh
poetry install --no-root
cp fastapi/fastapi.env.tmpl fastapi/fastapi.env
```

```bash
docker compose up --build
```

Services
FastAPI → http://localhost:8000


Django Admin → http://localhost:8001/admin

Default Admin User
Email: admin@example.com

Password: Admin123

API Endpoints
Auth
POST /api/auth/login

Users
GET /api/user/

Registraton
POST /api/user/

Health
GET /api/health/

Blocks
GET /api/block/blocks

GET /api/block/block

GET /api/block/providers

Crypto Stats
GET /api/crypto/stats/

GET /api/crypto/stats/latest

Background Tasks
Celery worker + beat fetch BTC/ETH data every minute and store it in DB.
Duplicates are prevented.
