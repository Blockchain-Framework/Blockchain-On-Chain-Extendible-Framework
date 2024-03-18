class APIResponse:
    def __init__(self, status, data=None, error=None, page_size=None, total_pages=None, current_page=None, total_items=None):
        self.status = status
        self.data = data
        self.error = error
        self.page_size = page_size
        self.total_pages = total_pages
        self.current_page = current_page
        self.total_items = total_items

    def to_dict(self):
        response = {
            "status": self.status,
            "data": self.data,
            "error": self.error,
        }
        if self.page_size is not None:  # Pagination info is optional
            pagination_info = {
                "page_size": self.page_size,
                "total_pages": self.total_pages,
                "current_page": self.current_page,
                "total_items": self.total_items,
            }
            response["pagination"] = pagination_info
        return response
