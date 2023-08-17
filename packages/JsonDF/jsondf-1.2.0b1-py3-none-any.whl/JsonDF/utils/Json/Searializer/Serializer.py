import JsonDF.utils.Json.Json as Json
import inspect

class Serializer:
    def __init__(self, object:object):
        self.object = object
    
    def get_name(self):
        return self.object.__name__
    
    def get_object_params(self):
        params = Json('params', {}).objectiy()
        attributes = inspect.getmembers(self.object, lambda a:not(inspect.isroutine(a)))
        for a in attributes:
            if not (a[0].startswith('__') and a[0].endswith('__')):
                params.insert(f"{a[0]}", a)
        return params
    
    def get_methods(self):
        methods = Json('methods', {}).objectiy()
        for key, value in self.object.__dict__.items():
            if callable(self.object.__dict__[key]):
                method_name = key
                method_params = self.get_method_params(value)
                method_code = self.get_code(value)
                methods.insert(f"{self.get_name()}.{method_name}", Json(f"{self.get_name()}.{method_name}", {f"{self.get_name()}.{method_name}": { 'params' : method_params, 'code': method_code }}).objectiy())
        return methods


    def get_method_params(self, method:classmethod) -> set:
        # print(method.__code__.co_varnames[:method.__code__.co_argcount])
        return (inspect.getfullargspec(method).args, inspect.getfullargspec(method).defaults)
    
    def get_code(self, method:classmethod) -> str:
        return inspect.getsource(method)
    
    def Serialize(self):
        return Json(self.get_name(), {'name': self.get_name(),
                                      'params': self.get_object_params(),
                                      'methods': self.get_methods()}).objectiy()