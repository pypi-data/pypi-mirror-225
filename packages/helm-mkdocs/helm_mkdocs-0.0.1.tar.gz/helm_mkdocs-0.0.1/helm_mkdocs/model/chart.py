class Chart:
    def __init__(self, dict):
        self.dict = dict

    def __getattr__(self, item):
        if item in self.dict:
            return self.dict[item]
        return None
