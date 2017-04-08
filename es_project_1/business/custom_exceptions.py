class Unauthorized(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


class Forbidden(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)


class NotFound(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)