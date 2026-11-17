import base64
from datetime import date

import pytest

from decorators import (
    Base64Decorator,
    DateDecorator,
    HeaderDecorator,
    MessageDecorator,
    SignatureDecorator,
)
from interfaces import BaseMessage
from messages import Message


def test_message_decorator_delegates() -> None:
    assert MessageDecorator(Message("hello")).render() == "hello"


def test_header_decorator_prepends() -> None:
    assert HeaderDecorator(Message("body"), "H").render() == "H\nbody"


def test_signature_decorator_appends() -> None:
    assert SignatureDecorator(Message("body"), "S").render() == "body\nS"


def test_date_decorator_with_explicit_date() -> None:
    assert (
        DateDecorator(Message("body"), "2025-01-01").render()
        == "body\n2025-01-01"
    )


def test_date_decorator_default_uses_today() -> None:
    expected = f"body\n{date.today().isoformat()}"
    assert DateDecorator(Message("body")).render() == expected


def test_base64_decorator() -> None:
    expected = base64.b64encode(b"hello").decode("ascii")
    assert Base64Decorator(Message("hello")).render() == expected


def test_decorators_combine() -> None:
    msg = HeaderDecorator(
        SignatureDecorator(
            HeaderDecorator(Message("body"), "H1"),
            "S",
        ),
        "H2",
    )
    assert msg.render() == "H2\nH1\nbody\nS"


def test_base64_over_combination() -> None:
    inner = HeaderDecorator(Message("body"), "H")
    expected = base64.b64encode("H\nbody".encode("utf-8")).decode("ascii")
    assert Base64Decorator(inner).render() == expected


@pytest.mark.parametrize(
    "msg",
    [
        HeaderDecorator(Message("x"), "h"),
        SignatureDecorator(Message("x"), "s"),
        DateDecorator(Message("x"), "2020-01-01"),
        Base64Decorator(Message("x")),
    ],
)
def test_decorators_are_base_message(msg: BaseMessage) -> None:
    assert isinstance(msg, BaseMessage)