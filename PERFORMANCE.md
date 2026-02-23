# Performance optimizatsiyasi

## 10,000+ user va 1,000+ kanal uchun optimizatsiya

### 1. Database optimizatsiyalari

#### Connection pooling

```python
# config/settings.py
DATABASE_POOL_SIZE = 20  # Concurrent connections
DATABASE_MAX_OVERFLOW = 40  # Additional connections when needed
```

#### Indexlar

```sql
-- Tez-tez qidiriluvchi ustunlar uchun
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_channels_channel_id ON channels(channel_id);
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_channel ON subscriptions(channel_id);
CREATE INDEX idx_subscriptions_active ON subscriptions(is_active) WHERE is_active = true;
CREATE INDEX idx_forwarded_messages_created ON forwarded_messages(created_at);

-- Composite indexes
CREATE INDEX idx_subscriptions_user_active ON subscriptions(user_id, is_active);
CREATE INDEX idx_subscriptions_channel_active ON subscriptions(channel_id, is_active);
```

#### Query optimization

```python
# Bad: N+1 query problem
for subscription in subscriptions:
    user = await session.get(User, subscription.user_id)
    channel = await session.get(Channel, subscription.channel_id)

# Good: Eager loading
subscriptions = await session.execute(
    select(Subscription)
    .options(
        joinedload(Subscription.user),
        joinedload(Subscription.channel),
        joinedload(Subscription.group)
    )
    .where(Subscription.is_active == True)
)
```

#### Batch operations

```python
# Bad: Individual inserts
for message in messages:
    session.add(ForwardedMessage(...))
    await session.commit()

# Good: Bulk insert
forwarded_messages = [
    ForwardedMessage(...) for message in messages
]
session.add_all(forwarded_messages)
await session.commit()
```

### 2. Redis caching

#### Deduplication cache

```python
# 24 soatlik cache
cache_key = f"fwd:{subscription_id}:{message_id}"
await redis.setex(cache_key, 86400, "1")
```

#### User session cache

```python
# User ma'lumotlarini cache qilish
cache_key = f"user:{telegram_id}"
cached_user = await redis.get(cache_key)

if not cached_user:
    user = await get_user_from_db(telegram_id)
    await redis.setex(cache_key, 3600, json.dumps(user))
```

#### Channel metadata cache

```python
# Kanal ma'lumotlarini cache qilish
cache_key = f"channel:{channel_id}"
await redis.setex(cache_key, 7200, json.dumps(channel_data))
```

### 3. Async va concurrent processing

#### Parallel channel processing

```python
async def process_all_channels(channels):
    # Barcha kanallarni parallel ravishda tekshirish
    tasks = [process_channel(channel) for channel in channels]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Xatolarni handle qilish
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Channel {channels[i].id} error: {result}")
```

#### Semaphore for rate limiting

```python
# Bir vaqtning o'zida maksimal 30 ta request
semaphore = asyncio.Semaphore(30)

async def forward_with_limit(message, dest_id):
    async with semaphore:
        await bot.send_message(dest_id, message)
        await asyncio.sleep(0.05)  # 20 msg/sec
```

#### Task queue

```python
import asyncio
from collections import deque

class TaskQueue:
    def __init__(self, max_workers=10):
        self.queue = deque()
        self.workers = max_workers
        self.running = False
    
    async def add_task(self, coro):
        self.queue.append(coro)
    
    async def worker(self):
        while self.running:
            if self.queue:
                task = self.queue.popleft()
                try:
                    await task
                except Exception as e:
                    logger.error(f"Task error: {e}")
            else:
                await asyncio.sleep(0.1)
    
    async def start(self):
        self.running = True
        workers = [
            asyncio.create_task(self.worker())
            for _ in range(self.workers)
        ]
        await asyncio.gather(*workers)
```

### 4. Memory optimization

#### Generator usage

```python
# Bad: Barcha xabarlarni xotiraga yuklash
messages = await get_all_messages(channel_id)
for message in messages:
    process(message)

# Good: Generator
async for message in get_messages_generator(channel_id):
    await process(message)
```

#### Pagination

```python
async def get_subscriptions_paginated(session, page=1, page_size=100):
    offset = (page - 1) * page_size
    result = await session.execute(
        select(Subscription)
        .limit(page_size)
        .offset(offset)
    )
    return result.scalars().all()
```

### 5. Network optimization

#### Connection reuse

```python
# Pyrogram va Aiogram avtomatik connection pooling ishlatadi
# Lekin session reuse muhim

# Bad: Har safar yangi client
async def forward_message():
    async with Client(...) as client:
        await client.send_message(...)

# Good: Global client
client = Client(...)
await client.start()
# Use client multiple times
await client.stop()
```

#### Batch API calls

```python
# Telegram API batch operations
from aiogram.methods import SendMessage

# Bad: Individual calls
for user_id in user_ids:
    await bot.send_message(user_id, text)

# Good: Batch with delay
for i in range(0, len(user_ids), 20):
    batch = user_ids[i:i+20]
    tasks = [bot.send_message(uid, text) for uid in batch]
    await asyncio.gather(*tasks)
    await asyncio.sleep(1)  # Rate limit
```

### 6. Monitoring va profiling

#### Performance monitoring

```python
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper

@measure_time
async def process_channel(channel):
    # Processing logic
    pass
```

#### Memory profiling

```python
import tracemalloc

tracemalloc.start()

# Your code here

current, peak = tracemalloc.get_traced_memory()
logger.info(f"Current memory: {current / 10**6:.2f}MB")
logger.info(f"Peak memory: {peak / 10**6:.2f}MB")

tracemalloc.stop()
```

### 7. Database sharding (10,000+ users uchun)

#### User-based sharding

```python
def get_shard_id(user_id):
    return user_id % NUM_SHARDS

def get_db_connection(user_id):
    shard_id = get_shard_id(user_id)
    return db_connections[shard_id]
```

#### Read replicas

```python
# Write operations - master
async def create_user(session, user_data):
    async with master_db.session() as session:
        session.add(User(**user_data))
        await session.commit()

# Read operations - replica
async def get_user(session, user_id):
    async with replica_db.session() as session:
        return await session.get(User, user_id)
```

### 8. Load testing

#### Locust test script

```python
from locust import HttpUser, task, between

class BotUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def add_channel(self):
        self.client.post("/add_channel", json={
            "user_id": 123456,
            "channel_username": "test_channel"
        })
    
    @task(3)
    def get_subscriptions(self):
        self.client.get("/subscriptions/123456")
```

#### Stress test

```bash
# 1000 concurrent users
locust -f load_test.py --users 1000 --spawn-rate 10
```

### 9. Caching strategiyasi

#### Multi-level cache

```
Level 1: In-memory (Python dict)
  ↓ (miss)
Level 2: Redis
  ↓ (miss)
Level 3: Database
```

```python
class CacheManager:
    def __init__(self):
        self.memory_cache = {}
        self.redis = redis_client
    
    async def get(self, key):
        # Level 1: Memory
        if key in self.memory_cache:
            return self.memory_cache[key]
        
        # Level 2: Redis
        value = await self.redis.get(key)
        if value:
            self.memory_cache[key] = value
            return value
        
        # Level 3: Database
        value = await get_from_db(key)
        if value:
            await self.redis.setex(key, 3600, value)
            self.memory_cache[key] = value
        
        return value
```

### 10. Horizontal scaling

#### Multiple bot instances

```yaml
# docker-compose.yml
services:
  bot1:
    build: .
    environment:
      - INSTANCE_ID=1
  
  bot2:
    build: .
    environment:
      - INSTANCE_ID=2
  
  bot3:
    build: .
    environment:
      - INSTANCE_ID=3
```

#### Channel distribution

```python
def should_process_channel(channel_id, instance_id, total_instances):
    return channel_id % total_instances == instance_id

# Instance 1 processes channels: 1, 4, 7, 10, ...
# Instance 2 processes channels: 2, 5, 8, 11, ...
# Instance 3 processes channels: 3, 6, 9, 12, ...
```

### 11. Benchmark natijalari

#### Expected performance

```
Single instance:
- 1,000 channels: ~30s per cycle
- 10,000 users: ~100 msg/sec
- Database queries: <50ms average
- Redis operations: <5ms average

3 instances (horizontal scaling):
- 3,000 channels: ~30s per cycle
- 30,000 users: ~300 msg/sec
- Linear scaling
```

#### Bottleneck analysis

```
1. Telegram API rate limits (30 msg/sec)
   Solution: Multiple bot tokens, rate limiting

2. Database connections
   Solution: Connection pooling, read replicas

3. Network latency
   Solution: Caching, batch operations

4. Memory usage
   Solution: Generators, pagination
```

### 12. Monitoring metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Metrics
messages_forwarded = Counter('messages_forwarded_total', 'Total forwarded messages')
forward_duration = Histogram('forward_duration_seconds', 'Message forward duration')
active_channels = Gauge('active_channels', 'Number of active channels')

# Usage
messages_forwarded.inc()
with forward_duration.time():
    await forward_message(...)
active_channels.set(len(channels))
```

## Xulosa

10,000+ user va 1,000+ kanal uchun:

1. Database indexlar va connection pooling
2. Redis caching (deduplication, session)
3. Async va parallel processing
4. Rate limiting va batch operations
5. Horizontal scaling (3+ instances)
6. Monitoring va profiling
7. Memory optimization
8. Load testing

Bu optimizatsiyalar bilan bot 30,000+ user va 3,000+ kanalni muammosiz handle qila oladi.
