from decorators import (
    Base64Decorator,
    DateDecorator,
    HeaderDecorator,
    SignatureDecorator,
)
from messages import Message
from proxies import ProtectedMessageProxy
from security import AccessPolicy, UserContext


def main() -> None:
    base = Message("С наступающим Новым годом!")

    # --- 1. Цепочка декораторов ---
    decorated = HeaderDecorator(
        SignatureDecorator(
            DateDecorator(
                HeaderDecorator(base, "===== Сообщение ====="),
                "2025-12-31",
            ),
            "— Иван Петров",
        ),
        "Уважаемый пользователь!",
    )

    print("=== Цепочка декораторов ===")
    print(decorated.render())
    print()

    # --- 2. Base64 поверх всей цепочки ---
    print("=== + Base64 ===")
    print(Base64Decorator(decorated).render())
    print()

    # --- 3. Proxy: успешный доступ ---
    policy = AccessPolicy("reader")
    alice = UserContext.of("alice", "reader")
    bob = UserContext.of("bob", "guest")

    print("=== Proxy: успешный доступ ===")
    print(ProtectedMessageProxy(decorated, policy, alice).render())
    print()

    # --- 4. Proxy: отказ в доступе ---
    print("=== Proxy: отказ в доступе ===")
    try:
        ProtectedMessageProxy(decorated, policy, bob).render()
    except PermissionError as exc:
        print(f"PermissionError: {exc}")


if __name__ == "__main__":
    main()