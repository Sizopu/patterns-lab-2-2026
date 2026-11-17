from interfaces import BaseMessage
from security import AccessPolicy, UserContext


class ProtectedMessageProxy(BaseMessage):
    """Proxy, контролирующий доступ к реальному сообщению.

    Не изменяет содержимое: только решает — пускать или нет.
    """

    def __init__(
        self,
        message: BaseMessage,
        policy: AccessPolicy,
        user: UserContext,
    ) -> None:
        self._message = message
        self._policy = policy
        self._user = user

    def render(self) -> str:
        if not self._policy.is_allowed(self._user):
            raise PermissionError(
                f"Пользователь {self._user.username!r} не имеет доступа"
            )
        return self._message.render()