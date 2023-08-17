

class OMNI_INFER_API_ERROR(Exception):
    messages: str

    def __init__(self, m: str):
        self.messages = m

    def __str__(self):
        return self.messages
