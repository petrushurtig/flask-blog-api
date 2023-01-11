from datetime import datetime

class IPost:
    id: int
    title: str
    content: str
    user_id: int
    views: int
    created_at: datetime
    updated_at: datetime

    def json(self):
        raise NotImplementedError