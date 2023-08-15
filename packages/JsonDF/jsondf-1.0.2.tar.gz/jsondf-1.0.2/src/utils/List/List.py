from ..Dict.Dict import Dict as d
class List:
    def __init__(self, prefix, data):
        self.data = data
        self.prefix = prefix
        self.rows = {}
        self.childs = self.process()

    
    def process(self):
        if len(self.data) > 1:
            self.data = self.data[0]
            self.childs(self.data)
        elif len(self.data) == 1:
            if type(self.data[0]) == dict:
                self.data = self.data[0]
                return self.childs(list(self.data.keys()))
            else:
                return self.data[0]
    
    def childs(self, keys):
        for key in keys:
            if type(self.data[key]) == list or type(self.data[key]) == dict:
                self.rows[f"{self.prefix}_{key}"] = self.childType(data=self.data[key], prefix=f"{self.prefix}_{key}")
            else:
                self.rows[f"{self.prefix}_{key}"] = self.data[key]
    
    def childType(self, data, prefix):
        if type(data) == list:
            return List(data=data, prefix=prefix).rows
        elif type(data) == dict:
            return d.Dict(data=data, prefix=prefix).rows
