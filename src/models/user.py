from src.interfaces.models.user import IUser

class User(IUser):
    id: int
    name: str
    email: str
    password: str
    info: dict
    bearer_token: str

    def __init__(
        self,
        id: str,
        info: dict,
        name=None,
        email=None,
        password=None,
        bearer_token=None
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.info = info
        self.bearer_token = bearer_token

    def json(self) -> dict:
        json_dict = vars(self)
        return json_dict
