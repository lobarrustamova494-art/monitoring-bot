# Deployment yo'riqnomasi

## VPS sozlash

### 1. Server talablari

- Ubuntu 20.04+ yoki Debian 11+
- Minimum 2GB RAM
- 20GB disk space
- Python 3.11+
- Docker va Docker Compose

### 2. Server sozlash

```bash
# Server yangilash
sudo apt update && sudo apt upgrade -y

# Docker o'rnatish
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Docker Compose o'rnatish
sudo apt install docker-compose -y

# User qo'shish
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Loyihani deploy qilish

```bash
# Repository clone
git clone <your-repo-url>
cd telegram-news-bot

# Environment sozlash
cp .env.example .env
nano .env  # O'zgaruvchilarni to'ldiring

# Bot tokenlarini olish
# 1. @BotFather dan BOT_TOKEN oling
# 2. https://my.telegram.org dan API_ID va API_HASH oling

# Docker build va run
docker-compose up -d

# Loglarni ko'rish
docker-compose logs -f bot
```

### 4. Database migratsiya

```bash
# Alembic sozlash
docker-compose exec bot alembic init alembic

# Migration yaratish
docker-compose exec bot alembic revision --autogenerate -m "Initial migration"

# Migration qo'llash
docker-compose exec bot alembic upgrade head
```

### 5. Pyrogram session yaratish

Birinchi marta ishga tushirganda, Pyrogram telefon raqamingizni so'raydi:

```bash
docker-compose exec -it bot python -c "from pyrogram import Client; from config import settings; app = Client('newsbot_session', api_id=settings.API_ID, api_hash=settings.API_HASH); app.start(); app.stop()"
```

Bu sizning telefon raqamingizga kod yuboradi. Kodni kiriting va session yaratiladi.

### 6. Monitoring

```bash
# Container statusini ko'rish
docker-compose ps

# Loglar
docker-compose logs -f

# Resource usage
docker stats

# Restart
docker-compose restart bot
```

## Production optimizatsiyalari

### 1. Nginx reverse proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. SSL sertifikat (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. Systemd service (Docker Compose uchun)

```bash
sudo nano /etc/systemd/system/newsbot.service
```

```ini
[Unit]
Description=News Bot
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/telegram-news-bot
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable newsbot
sudo systemctl start newsbot
```

### 4. Backup strategiyasi

```bash
# Database backup
docker-compose exec db pg_dump -U postgres newsbot > backup_$(date +%Y%m%d).sql

# Cron job qo'shish
crontab -e
# Har kuni soat 3 da backup
0 3 * * * cd /path/to/telegram-news-bot && docker-compose exec db pg_dump -U postgres newsbot > backups/backup_$(date +\%Y\%m\%d).sql
```

### 5. Monitoring va alerting

Prometheus + Grafana yoki simple health check:

```bash
# Health check script
#!/bin/bash
if ! docker-compose ps | grep -q "Up"; then
    echo "Bot is down! Restarting..."
    docker-compose restart bot
    # Send alert (Telegram, email, etc.)
fi
```

## Performance tuning

### PostgreSQL sozlamalari

`docker-compose.yml` da:

```yaml
db:
  command: postgres -c shared_buffers=256MB -c max_connections=200
```

### Redis sozlamalari

```yaml
redis:
  command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
```

## Troubleshooting

### Bot ishlamayapti

```bash
# Loglarni tekshiring
docker-compose logs bot

# Container restart
docker-compose restart bot

# Database connection
docker-compose exec db psql -U postgres -d newsbot
```

### Memory issues

```bash
# Memory usage
docker stats

# Restart services
docker-compose restart
```

### Database migration issues

```bash
# Reset migrations
docker-compose exec bot alembic downgrade base
docker-compose exec bot alembic upgrade head
```

## Xavfsizlik

1. `.env` faylini git ignore qiling
2. Strong parollar ishlating
3. Firewall sozlang:

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

4. Regular yangilanishlar:

```bash
# Weekly updates
sudo apt update && sudo apt upgrade -y
docker-compose pull
docker-compose up -d
```

## Scaling

10,000+ user uchun:

1. Database connection pool oshiring
2. Redis cache qo'shing
3. Multiple bot instances (load balancing)
4. Separate monitoring service

```yaml
# docker-compose.yml
bot:
  deploy:
    replicas: 3
```

## Support

Muammolar bo'lsa:
- Loglarni tekshiring: `docker-compose logs -f`
- GitHub Issues: <repo-url>/issues
- Telegram: @support
