class TokenExpired(Exception):
    def __init__(self, message = 'The token has expired') -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
    
class TokenGenerationException(Exception):
    def __init__(self, message = 'Token could not be generated') -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
    
class EmailSendingException(Exception):
    def __init__(self, message = 'Email wasn\'t sent') -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
    
class InvalidDomainException(Exception):
    def __init__(self, message = 'The token\'s domain does not match any of the allowed hosts') -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
    
class AlreadyVerifiedException(Exception):
    def __init__(self, message = 'This account has already been verified') -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message