from dataclasses import dataclass


@dataclass
class Response:
    ok: bool
    result: any = None
    error: dict = None
    panic: dict = None

    @property
    def is_valid(self):
        return self.ok or (not self.ok and not self.result and (self.error or self.panic))
