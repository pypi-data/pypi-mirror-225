import g4f


class NoProvider(Exception):
    """Called when there is no suitable provider for your requirements
    """
    def __init__(self, g4f_model: g4f.Model, message: str = 'No provider for {} model') -> None:
        super().__init__(message.format(g4f_model.name))
