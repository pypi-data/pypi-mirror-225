class Json:
    def __init__(self, name, json={}):
        self.json = json
        self.name = name
    
    def objectiy(self):
        keys = self.json.keys()
        for key in keys:
            value = self.value(self.json[key])
            self.__setattr__(key, value)
        return self
    
    def value(self, value):
        if type(value) == dict or type(value) == list:
            if type(value) == list:
                return [self.process(value)]
            else:
                return Json(0, value).objectiy()
        else:
            return value

    def process(self, value):
        if value == None: return []
        for val in value:
            if type(val) == dict:
                return Json(0, val).objectiy()

    def __repr__(self):
        return self.json.__str__()