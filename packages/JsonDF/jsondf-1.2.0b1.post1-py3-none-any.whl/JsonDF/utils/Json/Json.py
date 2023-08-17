class Json:
    def __init__(self, name, json={}, depth=0):
        self.json = json
        self.json_name = name
        self.__depth__ = depth
        self.__total_depth__ = 0
        self.__depth_in__ = []
    
    def objectiy(self):
        keys = self.json.keys()
        for key in keys:
            value = self.__value(self.json[key], key)
            self.__setattr__(key, value)
        return self
    
    def insert(self, name, value):
        self.__setattr__(name, value)
        return self
    
    def delete(self, name):
        del self.__dict__[name]
        return self
    
    def dump(self, name):
        valueType = type(self.__getattribute__(name))
        if valueType == Json:
            self.__total_depth__ += 1
            self.__depth_in__.append(self.name)
            self.__setattr__(name, Json(0, {}, self.__depth__+1))
        elif valueType == list:
            self.__setattr__(name, [])
        elif valueType == dict:
            self.__setattr__(name, {})
        elif valueType == str:
            self.__setattr__(name, '')
        else:
            self.__setattr__(name, 0)
        return self
    
    def find(self, name, report=False):
        try:
            value = self.__getattribute__(name)
            return (value, True) if report else value
        except:
            return ((self.__depth__, f"No results for {name} in {self.json_name} at depth {self.__depth__}"), False) if report else f"No results for {name} in {self.json_name} at depth {self.__depth__}"
    def find_all(self, name, reports=True):
        query = {}
        result = self.find(name, True)
        if result[1]:
            query[(self.__depth__, name, self.json_name)] = self.find(name, True)[0]
            print(query)
        else:
            if reports: print(result[0][1])

        if self.depth_check(self):
            for depth_point in self.__depth_in__:
                if type(self.__getattribute__(depth_point)) == list:
                    self.__getattribute__(depth_point)[0].find_all(name, reports)
                else:
                    self.__getattribute__(depth_point).find_all(name, reports)
        
        return query
    
    def depth_check(self, json:object):
        if json.__total_depth__ > 0:
            return True
        return False

    def __value(self, value, key):
        if type(value) == dict or type(value) == list:
            if type(value) == list:
                return [self.process(value, key)]
            else:
                self.__total_depth__ += 1
                self.__depth_in__.append(key)
                return Json(key, value, self.__depth__+1).objectiy()
        else:
            return value

    def process(self, value, key):
        if value == None: return []
        for val in value:
            if type(val) == dict:
                self.__total_depth__ += 1
                self.__depth_in__.append(key)
                return Json(key, val, self.__depth__+1).objectiy()
    
    def show(self):
        attrs = {}
        for attr in vars(self):
            if attr.startswith('__') or callable(attr) or attr == 'json' or attr == 'json_name':
                continue
            attrs[attr] = getattr(self, attr)
        return attrs

    def __repr__(self):
        return self.show().__str__()