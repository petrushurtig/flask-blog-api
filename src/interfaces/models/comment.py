from datetime import datetime

class IComment:
    id: int
    username: str
    content: str
    post_id: int
    created_at: datetime
    updated_at: datetime

    def json(self):
        raise NotImplementedError