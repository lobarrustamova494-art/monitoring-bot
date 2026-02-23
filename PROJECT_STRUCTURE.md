# Loyiha strukturasi

```
telegram-news-bot/
│
├── 📁 alembic/                      # Database migrations
│   ├── env.py                       # Alembic environment
│   ├── script.py.mako              # Migration template
│   └── versions/                    # Migration files
│
├── 📁 bot/                          # Bot handlers va UI
│   ├── __init__.py
│   ├── keyboards.py                # Inline keyboards
│   └── 📁 handlers/
│       ├── __init__.py
│       ├── start.py                # /start, help, main menu
│       ├── channels.py             # Kanal qo'shish, sozlash
│       ├── groups.py               # Guruh bilan ishlash
│       └── statistics.py           # Statistika ko'rsatish
│
├── 📁 config/                       # Konfiguratsiya
│   ├── __init__.py
│   └── settings.py                 # Environment settings
│
├── 📁 database/                     # Database layer
│   ├── __init__.py
│   ├── models.py                   # SQLAlchemy models
│   └── database.py                 # Database manager
│
├── 📁 services/                     # Business logic
│   ├── __init__.py
│   ├── user_service.py             # User CRUD
│   ├── channel_service.py          # Channel management
│   └── monitoring_service.py       # Channel monitoring
│
├── 📁 logs/                         # Log files (auto-created)
│   └── bot.log
│
├── 📄 main.py                       # Entry point
├── 📄 requirements.txt              # Python dependencies
├── 📄 Dockerfile                    # Docker image
├── 📄 docker-compose.yml            # Docker orchestration
├── 📄 .env.example                  # Environment template
├── 📄 .gitignore                    # Git ignore rules
├── 📄 alembic.ini                   # Alembic config
│
├── 📄 README.md                     # Loyiha haqida
├── 📄 ARCHITECTURE.md               # Arxitektura dokumentatsiyasi
├── 📄 DEPLOYMENT.md                 # Deployment yo'riqnomasi
├── 📄 WORKFLOW.md                   # Ishlash algoritmi
├── 📄 PERFORMANCE.md                # Performance optimizatsiyasi
└── 📄 PROJECT_STRUCTURE.md          # Bu fayl
```

## Fayl va papkalar tavsifi

### Root level

- **main.py**: Botning asosiy entry point. Bot va userbot initialization, handler registration, monitoring service start.

- **requirements.txt**: Python dependencies (aiogram, pyrogram, sqlalchemy, redis, etc.)

- **Dockerfile**: Docker image yaratish uchun instructions

- **docker-compose.yml**: Multi-container orchestration (bot, postgres, redis)

- **.env.example**: Environment variables template

- **alembic.ini**: Database migration tool configuration

### bot/ - Bot handlers va UI

- **keyboards.py**: Barcha inline keyboard layouts (main menu, channel list, settings, etc.)

- **handlers/start.py**: 
  - `/start` command
  - Main menu
  - Help
  - Cancel actions

- **handlers/channels.py**:
  - Kanal qo'shish (FSM)
  - Kanal ro'yxati
  - Kanal sozlamalari
  - Forward mode tanlash
  - Filtrlar
  - Kanal o'chirish

- **handlers/groups.py**:
  - Guruh ro'yxati
  - Bot guruhga qo'shilganda handler
  - Guruh sozlamalari

- **handlers/statistics.py**:
  - User statistikasi
  - Top kanallar
  - Yuborilgan postlar soni

### config/ - Konfiguratsiya

- **settings.py**: 
  - Environment variables
  - Pydantic settings
  - Database URL
  - Redis URL
  - Bot limits
  - Admin IDs

### database/ - Database layer

- **models.py**: SQLAlchemy ORM models
  - User
  - Channel
  - UserGroup
  - Subscription
  - ForwardedMessage
  - Enums (ForwardMode, FilterType)

- **database.py**:
  - DatabaseManager class
  - Connection pooling
  - Session management
  - Database initialization

### services/ - Business logic

- **user_service.py**:
  - get_or_create_user()
  - get_user_by_telegram_id()
  - update_premium_status()

- **channel_service.py**:
  - add_channel()
  - subscribe_user()
  - get_user_subscriptions()
  - unsubscribe()

- **monitoring_service.py**:
  - start_monitoring() - Main loop
  - _check_channels() - Barcha kanallarni tekshirish
  - _process_channel() - Bitta kanalni process qilish
  - _forward_message() - Xabarni forward qilish
  - _apply_filters() - Filtrlarni qo'llash
  - _forward_media_message() - Media forward

### alembic/ - Database migrations

- **env.py**: Alembic environment setup
- **versions/**: Migration files (auto-generated)

### Dokumentatsiya

- **README.md**: Loyiha haqida umumiy ma'lumot, quick start

- **ARCHITECTURE.md**: 
  - Arxitektura diagrammasi
  - Database schema
  - Komponentlar
  - Data flow
  - Performance optimizatsiyalari
  - Scaling strategiyasi

- **DEPLOYMENT.md**:
  - VPS sozlash
  - Docker deployment
  - Production optimizatsiyalari
  - Backup strategiyasi
  - Monitoring
  - Troubleshooting

- **WORKFLOW.md**:
  - Bot lifecycle
  - User interaction flow
  - Monitoring service flow
  - Filter logic
  - Message forwarding
  - Error handling

- **PERFORMANCE.md**:
  - Database optimizatsiyalari
  - Redis caching
  - Async processing
  - Memory optimization
  - Load testing
  - Horizontal scaling

## Kod organizatsiyasi

### Separation of concerns

```
Presentation Layer (bot/handlers/)
        ↓
Business Logic (services/)
        ↓
Data Access (database/)
        ↓
Database (PostgreSQL)
```

### Dependency injection

```python
# Middleware orqali
@dp.update.outer_middleware()
async def db_session_middleware(handler, event, data):
    async with db_manager.async_session() as session:
        data["session"] = session
        data["userbot"] = userbot
        return await handler(event, data)

# Handler da
async def cmd_start(message: Message, session: AsyncSession):
    # session va userbot avtomatik inject qilinadi
```

### Async/await pattern

Barcha I/O operations async:
- Database queries
- Redis operations
- Telegram API calls
- File operations

### Error handling

```python
try:
    # Operation
except SpecificError as e:
    logger.error(f"Error: {e}")
    # Handle gracefully
except Exception as e:
    logger.exception("Unexpected error")
    # Fallback
```

## Development workflow

### 1. Local development

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup .env
cp .env.example .env
# Edit .env

# Run locally
python main.py
```

### 2. Testing

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Load tests
locust -f tests/load_test.py
```

### 3. Docker development

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f bot

# Stop
docker-compose down
```

### 4. Database migrations

```bash
# Create migration
docker-compose exec bot alembic revision --autogenerate -m "Description"

# Apply migration
docker-compose exec bot alembic upgrade head

# Rollback
docker-compose exec bot alembic downgrade -1
```

## Best practices

### 1. Code style

- PEP 8 compliance
- Type hints
- Docstrings
- Meaningful variable names

### 2. Git workflow

```bash
# Feature branch
git checkout -b feature/new-feature

# Commit
git commit -m "feat: add new feature"

# Push
git push origin feature/new-feature

# Pull request
# Code review
# Merge to main
```

### 3. Environment variables

- Never commit .env
- Use .env.example as template
- Validate required variables on startup

### 4. Logging

- Use appropriate log levels
- Structured logging
- Log rotation
- Don't log sensitive data

### 5. Security

- No hardcoded secrets
- Input validation
- SQL injection prevention (ORM)
- Rate limiting
- Error messages (don't expose internals)

## Kengaytirish

### Yangi handler qo'shish

1. `bot/handlers/` da yangi fayl yarating
2. Router yarating
3. Handler funksiyalarni yozing
4. `bot/handlers/__init__.py` ga qo'shing
5. `main.py` da register qiling

### Yangi service qo'shish

1. `services/` da yangi fayl yarating
2. Service class yarating
3. Static methods yoki instance methods
4. `services/__init__.py` ga qo'shing

### Yangi model qo'shish

1. `database/models.py` ga model qo'shing
2. Migration yarating: `alembic revision --autogenerate`
3. Migration qo'llang: `alembic upgrade head`

## Xulosa

Loyiha modular, scalable va maintainable arxitektura bilan qurilgan. Har bir komponent o'z mas'uliyatiga ega va boshqa komponentlardan ajratilgan. Bu kelajakda yangi funksiyalar qo'shish va kodni maintain qilishni osonlashtiradi.
