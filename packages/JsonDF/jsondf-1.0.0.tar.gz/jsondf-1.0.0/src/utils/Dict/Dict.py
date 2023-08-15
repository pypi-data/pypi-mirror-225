import JsonDF.src.utils.List.List as l

class Dict:
    def __init__ (self, data, prefix):
        self.data = data
        self.prefix = prefix
        self.rows = {}
        self.childs = self.process()
    
    def process(self):
        if len(self.data.keys()) >= 1:
            return self.childs(list(self.data.keys()))
    
    def childs(self, keys):
        for key in keys:
            if type(self.data[key]) == list or type(self.data[key]) == dict:
                self.rows[f"{self.prefix}_{key}"] = self.childType(data=self.data[key], prefix=f"{self.prefix}_{key}")
            else:
                self.rows[f"{self.prefix}_{key}"] = self.data[key]

    def childType(self, data, prefix):
        if type(data) == list:
            return l.List(data=data, prefix=prefix).rows
        elif type(data) == dict:
            return Dict(data=data, prefix=prefix).rows