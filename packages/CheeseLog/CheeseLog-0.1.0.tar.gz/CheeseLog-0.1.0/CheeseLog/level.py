class Level:
    def __init__(self, weight: int, messageTemplate: str | None = None, timerTemplate: str | None = None, styledMessageTemplate: str | None = None):
        self.weight: int = weight
        self.messageTemplate: str | None = messageTemplate
        self.styledMessageTemplate: str | None = styledMessageTemplate
        self.timerTemplate: str | None = timerTemplate
