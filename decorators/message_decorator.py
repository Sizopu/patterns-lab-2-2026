from __future__ import annotations

import base64
from abc import ABC
from datetime import date

from interfaces import BaseMessage


class MessageDecorator(BaseMessage, ABC):
    """Базовый декоратор: хранит ссылку на другой BaseMessage."""

    def __init__(self, message: BaseMessage) -> None:
        self._message = message

    def render(self) -> str:
        return self._message.render()


class HeaderDecorator(MessageDecorator):
    """Добавляет заголовок перед сообщением."""

    def __init__(self, message: BaseMessage, header: str) -> None:
        super().__init__(message)
        self._header = header

    def render(self) -> str:
        return f"{self._header}\n{self._message.render()}"


class SignatureDecorator(MessageDecorator):
    """Добавляет подпись после сообщения."""

    def __init__(self, message: BaseMessage, signature: str) -> None:
        super().__init__(message)
        self._signature = signature

    def render(self) -> str:
        return f"{self._message.render()}\n{self._signature}"


class DateDecorator(MessageDecorator):
    """Добавляет дату после сообщения.

    Если дата не передана явно — используется текущая дата (ISO-формат).
    Возможность передать дату параметром нужна для детерминированных тестов.
    """

    def __init__(self, message: BaseMessage, value: str | None = None) -> None:
        super().__init__(message)
        self._value = value

    def render(self) -> str:
        value = self._value if self._value is not None else date.today().isoformat()
        return f"{self._message.render()}\n{value}"


class Base64Decorator(MessageDecorator):
    """Кодирует итоговый текст в Base64."""

    def render(self) -> str:
        raw = self._message.render().encode("utf-8")
        return base64.b64encode(raw).decode("ascii")