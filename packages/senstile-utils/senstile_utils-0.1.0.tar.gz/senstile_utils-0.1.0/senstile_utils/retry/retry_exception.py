class RetryException(Exception):
    def __init__(self, attempts_made: int, max_retries: int, last_exception: Exception, message="Maximum retry attempts reached"):
        self.attempts_made = attempts_made
        self.max_retries = max_retries
        self.last_exception = last_exception
        super().__init__(message)

    def __str__(self):
        original_message = super().__str__()
        return f"{original_message}. Attempts made: {self.attempts_made}/{self.max_retries}. Last exception: {self.last_exception}"
