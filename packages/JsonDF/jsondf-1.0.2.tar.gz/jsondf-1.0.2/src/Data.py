from .utils.Dict.Dict import Dict as d
from .utils.List.List import List as l
class Data:
    def __init__(self, prefix='root', data=dict()) -> None:
        self.data = data
        self.prefix = prefix
        self.rows = {}
        self.rows_flatten = {}
    
    def childs(self):
        if type(self.data) == dict: 
            if len(self.data.keys()) >= 1:
                self.childsType(list(self.data.keys()))
        if type(self.data) == list:
            if len(self.data) >= 1:
                self.data = self.data[0]
                self.childsType(self.data)
    
    def childsType(self, keys):
        for key in keys:
            if type(self.data[key]) == list or type(self.data[key]) == dict:
                self.rows[f"{self.prefix}_{key}"] = self.child(data=self.data[key], prefix=f"{self.prefix}_{key}")
            else:
                self.rows[f"{self.prefix}_{key}"] = self.data[key]
    
    def tabelize(self, rows):
        for key, value in rows.items():
            if type(value) == dict:
                yield from self.tabelize(value)
            else:
                yield(key, value)
    
    def flatten(self):
        for key, value in self.tabelize(self.rows):
            self.rows_flatten[key] = value


    def child(self, data, prefix):
        if type(data) == list:
            return l.List(data=data, prefix=prefix).rows
        elif type(data) == dict:
            return d.Dict(data=data, prefix=prefix).rows