from .base import BaseModel

class Error(BaseModel):

    def __init__(self,
        type=None,
        exception_code=None,
        developer_message=None,
        more_info_url=None,
        timestamp=None
    ):
        
        super().__init__()
        
        self.type = type
        self.exception_code = exception_code
        self.developer_message = developer_message
        self.more_info_url = more_info_url
        self.timestamp = timestamp