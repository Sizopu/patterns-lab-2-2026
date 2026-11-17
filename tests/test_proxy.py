import pytest

from decorators import HeaderDecorator
from messages import Message
from proxies import ProtectedMessageProxy
from security import AccessPolicy, UserContext


def _make_proxy(user: UserContext, message=None) -> ProtectedMessageProxy:
    return ProtectedMessageProxy(
        message if message is not None else Message("hello"),
        AccessPolicy("reader"),
        user,
    )


def test_proxy_allows_user_with_role() -> None:
    alice = UserContext.of("alice", "reader")
    assert _make_proxy(alice).render() == "hello"


def test_proxy_denies_user_without_role() -> None:
    bob = UserContext.of("bob", "guest")
    with pytest.raises(PermissionError):
        _make_proxy(bob).render()


def test_proxy_does_not_modify_content() -> None:
    text = "some text"
    alice = UserContext.of("alice", "reader")
    assert _make_proxy(alice, Message(text)).render() == text


def test_proxy_wraps_decorated_message() -> None:
    inner = HeaderDecorator(Message("body"), "H")
    alice = UserContext.of("alice", "reader")
    assert _make_proxy(alice, inner).render() == "H\nbody"


def test_proxy_denied_for_decorated_message() -> None:
    inner = HeaderDecorator(Message("body"), "H")
    bob = UserContext.of("bob", "guest")
    with pytest.raises(PermissionError):
        _make_proxy(bob, inner).render()