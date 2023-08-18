class EmptyMeta(type):
    def __str__(self):
        return '__empty__'


class Empty(metaclass=EmptyMeta):
    ...
