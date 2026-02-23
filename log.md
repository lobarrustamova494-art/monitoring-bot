File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 601, in create_engine
    dbapi = dbapi_meth(**dbapi_args)
            ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/psycopg2.py", line 690, in import_dbapi
    import psycopg2
ModuleNotFoundError: No module named 'psycopg2'
2026-02-23 13:04:02.130 | INFO     | __main__:run_web_server:20 - 🌐 Web server started on port 10000
Traceback (most recent call last):
  File "/app/start.py", line 41, in <module>
    start()
  File "/app/start.py", line 36, in start
    asyncio.run(run_bot())
  File "/usr/local/lib/python3.11/asyncio/runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/app/start.py", line 25, in run_bot
    from main import main
  File "/app/main.py", line 8, in <module>
    from database import db_manager
  File "/app/database/__init__.py", line 3, in <module>
    from .database import DatabaseManager, get_db, db_manager
  File "/app/database/database.py", line 39, in <module>
    db_manager = DatabaseManager()
                 ^^^^^^^^^^^^^^^^^
  File "/app/database/database.py", line 18, in __init__
    self.engine = create_async_engine(
                  ^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/engine.py", line 117, in create_async_engine
    sync_engine = _create_engine(url, **kw)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 2, in create_engine
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/deprecations.py", line 281, in warned
    return fn(*args, **kwargs)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 601, in create_engine
    dbapi = dbapi_meth(**dbapi_args)
            ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/psycopg2.py", line 690, in import_dbapi
    import psycopg2
ModuleNotFoundError: No module named 'psycopg2'