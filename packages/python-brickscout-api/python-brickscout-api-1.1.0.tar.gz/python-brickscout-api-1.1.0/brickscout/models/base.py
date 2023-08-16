import jsonpatch
import json
from typing import Union, Optional

class BaseModel:
    
    def __init__(self) -> None:
        self.has_error = False
        self.error = None
        
        # Keep track of all the patches made to the object
        # This is used to update the object on the server
        self.patches = []
        self.initial = True # Used to prevent patches from being added when the object is first created
    
    def construct_from_response(self, resp_data: dict) -> Union['BaseModel', 'ObjectListModel']:
        """ Construct an object from the returned response data. """
        from .utils import construct_object_from_data
        return construct_object_from_data(resp_data)
    
    def construct_error_from_response(self, response: dict) -> 'BaseModel':
        """ Construct an error object from the returned response data and attach it to a BaseModel. """
        from .utils import construct_error_from_data
        return construct_error_from_data(response)
    
    def __getattr__(self, name: str) -> None:
        """ Gets called when an attribute is not found. Always returns None."""
        return None
    
    def __setattr__(self, name: str, value: object) -> None:
        """ Gets called when an attribute is set. Adds a patch to the list if the value is different from the current value. """
        if not self.initial and name not in ['has_error', 'error', 'initial', 'patches'] and hasattr(self, name) and getattr(self, name) != value:
            new_patch = jsonpatch.JsonPatch.from_diff({name: getattr(self, name)}, {name: value})
            if new_patch: self.patches += new_patch.patch
        
        return super().__setattr__(name, value)
    
    def to_dict(self) -> dict:
        """ Returns a dict representation of the object. """
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
    
class ObjectListModel(BaseModel):
    
    def __init__(self, list: Optional[list] = None) -> None:
        super().__init__()
        self.list = list if list else []

    def add(self, item: object) -> list:
        self.list.append(item)
        return self.list
    
    def remove(self, item: object) -> list:
        self.list.remove(item)
        return self.list
    
    def iterator(self) -> list:
        return self.list