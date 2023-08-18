from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from autoapi.auth.interface import IAuthProvider


class DjangoRequestAuthProvider(IAuthProvider):
    def authorize(self, request: HttpRequest):
        self.user_context_var.set(
            request.user if not isinstance(request.user, AnonymousUser)
                         else None
        )
