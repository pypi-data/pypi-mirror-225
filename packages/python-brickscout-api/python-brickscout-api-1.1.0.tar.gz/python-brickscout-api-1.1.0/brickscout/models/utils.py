from typing import Union
from .base import ObjectListModel, BaseModel
from .errors import Error

def construct_object_from_data(data: Union[dict, list]) -> 'BaseModel':
    """ Construct an object from the given data. 
    
    :param data: the data to construct the object from.
    :type data: Union[dict, list]
    :return: the constructed object. Dict data will be converted to a BaseModel, list data will be converted to an ObjectListModel.
    :rtype: BaseModel or ObjectListModel
    """
    
    if isinstance(data, list):
        object = ObjectListModel()
        
        for item in data:
            if isinstance(item, dict) or isinstance(item, list):
                sub_object = construct_object_from_data(item)
                object.add(sub_object)
            else:
                object.add(item)
        
    elif isinstance(data, dict):
        object = BaseModel()
    
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                sub_object = construct_object_from_data(value)
                setattr(object, key, sub_object)
            else:   
                setattr(object, key, value)
    else:
        raise TypeError(f'Cannot construct object from data of type {type(data)}')
    
    setattr(object, 'initial', False)
    return object

def construct_error_from_data(data: dict) -> 'BaseModel':
    """ Construct an error object from the given data and attach it to a BaseModel. 
    
    :param data: the data to construct the error object from.
    :type data: dict
    :return: the BaseModel with the error object attached and the 'has_error' flag set to True.
    :rtype: BaseModel
    """
    
    type = data['type'] if 'type' in data else None
    exception_code = data['exceptionCode'] if 'exceptionCode' in data else None
    developer_message = data['developerMessage'] if 'developerMessage' in data else None
    more_info_url = data['moreInfoUrl'] if 'moreInfoUrl' in data else None
    timestamp = data['timeStamp'] if 'timeStamp' in data else None

    object = BaseModel()
    
    object.has_error = True
    object.error = Error(
        type=type,
        exception_code=exception_code,
        developer_message=developer_message,
        more_info_url=more_info_url,
        timestamp=timestamp
    )
    
    setattr(object, 'initial', False)
    return object