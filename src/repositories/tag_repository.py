from src.interfaces.models.tag import ITag
from src.interfaces.repositories.tag_repository import ITagRepository
from src.db.models.tag import Tag

class TagRepository(ITagRepository):

    def get_all_tags(self) -> "list[ITag]":
        return Tag.get_all_tags()

    def find_by_id(self, tag_id: int) -> ITag:
        return Tag.get_tag_by_id(tag_id)

    def get_tag_by_name(self, name: str) -> ITag:
        return Tag.get_tag_by_name(name)

    def create_tag(self, name: str) -> ITag:
        tag = Tag()

        tag.name = name
        tag.save()

        return tag