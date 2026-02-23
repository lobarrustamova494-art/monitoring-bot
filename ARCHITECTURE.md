# Arxitektura dokumentatsiyasi

## Umumiy arxitektura

```
┌─────────────────────────────────────────────────────────────┐
│                     Telegram Bot System                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         Main Application (main.py)       │
        │  - Bot initialization                    │
        │  - Userbot (Pyrogram) initialization     │
        │  - Service orchestration                 │
        └─────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
    ┌───────────────────┐       ┌───────────────────┐
    │   Bot Handlers    │       │  Monitoring       │
    │   (Aiogram 3.x)   │       │  Service          │
    │                   │       │  (Pyrogram)       │
    │ - /start          │       │                   │
    │ - Add channel     │       │ - Channel polling │
    │ - Settings        │       │ - Message forward │
    │ - Statistics      │       │ - Filtering       │
    └───────────────────┘       └───────────────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                ┌─────────────────────────┐
                │   Business Services     │
                │                         │
                │ - UserService           │
                │ - ChannelService        │
                │ - MonitoringService     │
                └─────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
    ┌───────────────────┐       ┌───────────────────┐
    │   PostgreSQL      │       │      Redis        │
    │   Database        │       │      Cache        │
    │                   │       │                   │
    │ - Users           │       │ - Deduplication   │
    │ - Channels        │       │ - Rate limiting   │
    │ - Subscriptions   │       │ - Session cache   │
    │ - Messages log    │       └───────────────────┘
    └───────────────────┘
```

## Database schema

```sql
-- Users jadvali
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    is_premium BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Channels jadvali
CREATE TABLE channels (
    id SERIAL PRIMARY KEY,
    channel_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    title VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    last_message_id INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User groups jadvali
CREATE TABLE user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    group_id BIGINT NOT NULL,
    group_title VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Subscriptions jadvali
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    channel_id INTEGER REFERENCES channels(id) ON DELETE CASCADE,
    group_id INTEGER REFERENCES user_groups(id) ON DELETE SET NULL,
    forward_mode VARCHAR(20) DEFAULT 'private',
    filter_type VARCHAR(20) DEFAULT 'all',
    keyword_filter TEXT,
    add_prefix VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    posts_forwarded INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Forwarded messages log
CREATE TABLE forwarded_messages (
    id SERIAL PRIMARY KEY,
    subscription_id INTEGER REFERENCES subscriptions(id) ON DELETE CASCADE,
    channel_message_id INTEGER NOT NULL,
    forwarded_message_id INTEGER,
    destination_chat_id BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_channels_channel_id ON channels(channel_id);
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_channel ON subscriptions(channel_id);
CREATE INDEX idx_forwarded_messages_created ON forwarded_messages(created_at);
```

## Komponentlar

### 1. Bot Handlers (Aiogram)

User bilan interaksiya uchun:
- Command handlers (/start, /help)
- Callback query handlers (inline buttons)
- FSM (Finite State Machine) for multi-step operations
- Middleware for dependency injection

### 2. Monitoring Service (Pyrogram)

Real-time channel monitoring:
- Pyrogram MTProto API orqali kanallarni kuzatish
- Yangi xabarlarni aniqlash
- Filtrlar qo'llash
- Forward qilish

### 3. Business Services

- **UserService**: User CRUD operations
- **ChannelService**: Channel management, subscriptions
- **MonitoringService**: Channel polling, message forwarding

### 4. Database Layer

- SQLAlchemy ORM (async)
- Connection pooling
- Migration support (Alembic)

### 5. Cache Layer (Redis)

- Message deduplication
- Rate limiting
- Session caching

## Data flow

### Kanal qo'shish flow

```
User → /add_channel → FSM State
  ↓
User sends channel link
  ↓
Pyrogram checks channel
  ↓
Channel saved to DB
  ↓
Subscription created
  ↓
Success message
```

### Monitoring flow

```
Monitoring Service (loop every 30s)
  ↓
Get all active channels from DB
  ↓
For each channel:
  ↓
  Get new messages (Pyrogram)
  ↓
  Get subscriptions for channel
  ↓
  For each subscription:
    ↓
    Apply filters
    ↓
    Check Redis cache (dedup)
    ↓
    Forward message (Aiogram)
    ↓
    Log to DB
    ↓
    Update cache
```

## Performance optimizatsiyalari

### 1. Database

- Connection pooling (20 connections, 40 overflow)
- Indexes on frequently queried columns
- Batch operations where possible

### 2. Caching

- Redis for deduplication (24h TTL)
- In-memory cache for frequently accessed data

### 3. Async operations

- All I/O operations are async
- Concurrent processing of channels
- Non-blocking message forwarding

### 4. Rate limiting

- Telegram API limits respected
- Batch processing with delays
- Queue system for high load

## Scaling strategiyasi

### Horizontal scaling

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Bot 1  │     │  Bot 2  │     │  Bot 3  │
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     └───────────────┴───────────────┘
                     │
            ┌────────┴────────┐
            ▼                 ▼
     ┌──────────┐      ┌──────────┐
     │PostgreSQL│      │  Redis   │
     └──────────┘      └──────────┘
```

### Load balancing

- Multiple bot instances
- Shared database and cache
- Channel distribution across instances

### Database sharding

10,000+ users uchun:
- User-based sharding
- Read replicas
- Write-ahead logging

## Xavfsizlik

### 1. Authentication

- Bot token secure storage
- API credentials in environment variables
- No hardcoded secrets

### 2. Authorization

- User-based access control
- Admin-only commands
- Channel ownership verification

### 3. Data protection

- Encrypted connections (SSL/TLS)
- Password hashing
- Secure session storage

### 4. Rate limiting

- Per-user rate limits
- Global rate limits
- Anti-spam measures

## Monitoring va logging

### Logging levels

- INFO: Normal operations
- WARNING: Potential issues
- ERROR: Errors that need attention
- DEBUG: Detailed debugging info

### Metrics

- Active users count
- Channels monitored
- Messages forwarded
- Error rate
- Response time

### Health checks

- Database connectivity
- Redis connectivity
- Telegram API status
- Disk space
- Memory usage

## Error handling

### Retry strategy

```python
@retry(max_attempts=3, delay=1, backoff=2)
async def forward_message(...):
    # Forward logic
```

### Graceful degradation

- Continue on non-critical errors
- Log errors for later analysis
- Notify admins on critical failures

### Recovery

- Automatic reconnection
- State persistence
- Transaction rollback on errors

## Testing strategiyasi

### Unit tests

- Service layer tests
- Database operations
- Filter logic

### Integration tests

- Bot handlers
- Monitoring service
- End-to-end flows

### Load testing

- Simulate 10,000+ users
- Concurrent channel monitoring
- Database performance

## Deployment pipeline

```
Code → Git Push → CI/CD → Docker Build → Deploy → Health Check
```

### CI/CD

- Automated testing
- Docker image building
- Deployment to VPS
- Rollback on failure
