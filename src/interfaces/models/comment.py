from datetime import datetime

class IComment:
    id: int
    content: str
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    def json(self):
        raise NotImplementedError