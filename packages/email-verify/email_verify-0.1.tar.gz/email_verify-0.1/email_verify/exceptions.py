class TokenExpired(Exception):
    def __init__(self, message = 'The token has expired') -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
    
class InvalidDomain(Exception):
    def __init__(self, message = 'The token\'s domain does not match any of the allowed hosts') -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
    
class AlreadyVerified(Exception):
    def __init__(self, message = 'This account has already been verified') -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message