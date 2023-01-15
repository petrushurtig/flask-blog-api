from datetime import datetime
from typing import Any

class IPost:
    id: int
    title: str
    content: str
    user_id: int
    views: int
    created_at: datetime
    updated_at: datetime
    user: Any
    comments: Any
    tags: Any

    def json(self):
        raise NotImplementedError