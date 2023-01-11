from datetime import datetime

class IUser:
    id: int
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime

    def json(self):
        raise NotImplementedError