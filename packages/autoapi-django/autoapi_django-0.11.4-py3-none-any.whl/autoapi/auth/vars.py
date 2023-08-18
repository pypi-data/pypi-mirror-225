from contextvars import ContextVar

authorized_user = ContextVar('authorized_user', default=None)
