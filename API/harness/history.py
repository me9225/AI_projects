class ConversationHistory:
    def __init__(self):
        self.messages = []
    def add(self, message: dict):
        self.messages.append(message)
    def extend(self, messages: list[dict]):
        self.messages.extend(messages)
    def as_list(self):
        return list(self.messages)
    def compact(self, keep_last: int = 8):
        if len(self.messages) > keep_last:
            # Keep only recent messages; use only after a completed tool cycle.
            self.messages = self.messages[-keep_last:]
