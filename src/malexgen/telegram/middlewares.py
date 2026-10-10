

import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from ..utils.logger import logger


class LoggingMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_id = None
        username = None

        if isinstance(event, Message):
            user_id = event.from_user.id if event.from_user else None
            username = event.from_user.username if event.from_user else None
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            username = event.from_user.username

        start = time.time()

        try:
            result = await handler(event, data)
            elapsed = (time.time() - start) * 1000
            logger.debug(
                f"[TG] user={user_id} (@{username}) "
                f"event={type(event).__name__} "
                f"elapsed={elapsed:.1f}ms"
            )
            return result
        except Exception as e:
            logger.error(
                f"[TG] Error for user={user_id}: {e}"
            )
            raise


class RateLimitMiddleware(BaseMiddleware):

    def __init__(self, min_interval: float = 0.5):
        self.min_interval = min_interval
        self._last_call: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_id = None

        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

        if user_id:
            now = time.time()
            last = self._last_call.get(user_id, 0)

            if now - last < self.min_interval:
                logger.debug(f"[TG] Rate limited user={user_id}")
                return None

            self._last_call[user_id] = now

        return await handler(event, data)


__all__ = ["LoggingMiddleware", "RateLimitMiddleware"]
