
class ICommand:
    def execute(self, **kwargs) -> None:
        raise NotImplementedError