class PreconditionError(ValueError):
    """PRE non respectée."""
    pass


class PostconditionError(RuntimeError):
    """POST non respectée."""
    pass
