class FrameworkException(Exception):
    """Base class for all framework exceptions."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)