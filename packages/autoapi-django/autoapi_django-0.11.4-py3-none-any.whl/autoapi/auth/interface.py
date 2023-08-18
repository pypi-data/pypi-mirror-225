from abc import ABC, abstractmethod
from contextvars import ContextVar

from django.http import HttpRequest


class IAuthProvider(ABC):
    user_context_var: ContextVar

    @abstractmethod
    def authorize(self, request: HttpRequest):
        """
        Достает пользователя из запроса и кладет
        в заданную переменную контекста
        """
