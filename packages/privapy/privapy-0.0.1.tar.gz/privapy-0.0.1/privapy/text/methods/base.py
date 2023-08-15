class BaseMethod:
    replacement: str

    def __call__(self, *args, **kwargs):
        raise NotImplementedError
