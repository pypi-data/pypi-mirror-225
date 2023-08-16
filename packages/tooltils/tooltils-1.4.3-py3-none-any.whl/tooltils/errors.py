"""Package specific exceptions"""

class TooltilsError(Exception):
    """Base error class for tooltils specific errors"""

class ShellCodeError(TooltilsError):
    """Shell command returned non-zero exit code"""

    def __init__(self, code: int, 
                 message: str=''):
        self.message: str = message
        self.code:    int = code
    
    def __str__(self):
        if self.message:
            return self.message

        return 'Shell command returned non-zero exit code'

class ShellCommandError(TooltilsError):
    """Shell command exited while in process"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message

        return 'Shell command exited while in process'

class ShellTimeoutExpired(TooltilsError):
    """Shell command timed out"""
    
    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message

        return 'Shell command timed out'

class ConnectionError(TooltilsError):
    """Connection to URL failed"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message

        return 'Connection to URL failed'

class TimeoutExpired(TooltilsError):
    """Request read timeout expired"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message

        return 'Request read timeout expired'

class StatusCodeError(TooltilsError):
    """Status code of URL response is not 200"""
    
    def __init__(self, 
                 code: int, 
                 reason: str):
        self.code:   int = code
        self.reason: str = reason

    def __str__(self):
        return '{} {}'.format(self.code, self.reason)

class UnicodeDecodeError(TooltilsError):
    """Unable to decode text input"""

    def __init__(self, message: str=''):
        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message

        return 'Unable to decode text input'

