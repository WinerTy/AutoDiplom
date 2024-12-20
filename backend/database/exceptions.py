class OutOfCount(Exception):
    def __init__(self, message, auto_part_name, auto_part_count):
        self._message = None
        self.auto_part_name = auto_part_name
        self.auto_part_count = auto_part_count
        super().__init__(self.message)

    @property
    def message(self):
        if self._message is None:
            return (
                f"Товара '{self.auto_part_name}' недостаточно на складе. "
                f"Доступно: {self.auto_part_count}"
            )
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
