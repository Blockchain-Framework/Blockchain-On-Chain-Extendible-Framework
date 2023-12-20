class Response:
    def __init__(self, status, data=None, page_size=None, error=None):
        self.status = status
        self.data = data
        self.page_size = page_size
        self.error = error

    def to_dict(self):
        return {
            "status": self.status,
            "data": self.data,
            "page_size": self.page_size,
            "error": self.error
        }
