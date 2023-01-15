from src.interfaces.models.tag import ITag

class ITagRepository:
    def find_by_id(self, tag_id: int) -> ITag:
        raise NotImplementedError

    def get_tag_by_name(self, name: str) -> ITag:
        raise NotImplementedError

    def create_tag(self, name: str) -> ITag:
        raise NotImplementedError