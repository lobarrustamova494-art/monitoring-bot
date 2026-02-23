Cause exception while process update id=571278589 by bot id=8473209623
MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place? (Background on this error at: https://sqlalche.me/e/20/xd2s)
Traceback (most recent call last):
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\dispatcher.py", line 309, in _process_update
    response = await self.feed_update(bot, update, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\dispatcher.py", line 158, in feed_update
    response = await self.update.wrap_outer_middleware(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\middlewares\error.py", line 25, in __call__
    return await handler(event, data)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\middlewares\user_context.py", line 27, in __call__
    return await handler(event, data)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\fsm\middleware.py", line 41, in __call__
    return await handler(event, data)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Bots\News bot\main.py", line 52, in db_session_middleware
    return await handler(event, data)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\event\telegram.py", line 121, in trigger
    return await wrapped_inner(event, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\event\handler.py", line 43, in call
    return await wrapped()
           ^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\dispatcher.py", line 276, in _listen_update
    return await self.propagate_event(update_type=update_type, event=event, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\router.py", line 128, in propagate_event
    return await observer.wrap_outer_middleware(_wrapped, event=event, data=kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\router.py", line 123, in _wrapped
    return await self._propagate_event(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\router.py", line 156, in _propagate_event
    response = await router.propagate_event(update_type=update_type, event=event, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\router.py", line 128, in propagate_event
    return await observer.wrap_outer_middleware(_wrapped, event=event, data=kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\router.py", line 123, in _wrapped
    return await self._propagate_event(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\router.py", line 148, in _propagate_event
    response = await observer.trigger(event, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\event\telegram.py", line 121, in trigger
    return await wrapped_inner(event, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\aiogram\dispatcher\event\handler.py", line 43, in call
    return await wrapped()
           ^^^^^^^^^^^^^^^
  File "D:\Bots\News bot\bot\handlers\statistics.py", line 57, in show_statistics
    channel_name = sub.channel.title or sub.channel.username
                   ^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\attributes.py", line 566, in __get__
    return self.impl.get(state, dict_)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\attributes.py", line 1086, in get
    value = self._fire_loader_callables(state, key, passive)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\attributes.py", line 1121, in _fire_loader_callables
    return self.callable_(state, passive)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\strategies.py", line 967, in _load_for_state
    return self._emit_lazyload(
           ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\strategies.py", line 1068, in _emit_lazyload
    return loading.load_on_pk_identity(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\loading.py", line 692, in load_on_pk_identity
    session.execute(
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
    return meth(
           ^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1639, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 2347, in _handle_dbapi_exception
    raise exc_info[1].with_traceback(exc_info[2])
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\sqlite\aiosqlite.py", line 146, in execute
    self._adapt_connection._handle_exception(error)
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\sqlite\aiosqlite.py", line 298, in _handle_exception
    raise error
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\sqlite\aiosqlite.py", line 123, in execute
    _cursor = self.await_(self._connection.cursor())
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 121, in await_only
    raise exc.MissingGreenlet(
sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place? (Background on this error at: https://sqlalche.me/e/20/xd2s)
Failed to fetch updates - TelegramNetworkError: HTTP Client says - Request timeout error
Sleep for 1.000000 seconds and try again... (tryings = 0, bot id = 8473209623)