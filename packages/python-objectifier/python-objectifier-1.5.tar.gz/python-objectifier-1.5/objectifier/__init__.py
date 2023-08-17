dict_item = dict

class convert_json_to_object:
    def __new__(self, item):
        if isinstance(item, dict_item):
            updated_dict = dict()
            for key, value in item.items():
                if isinstance(value, (dict_item, list)):
                    value = convert_json_to_object(value)
                setattr(updated_dict, key, value)
                    
            return updated_dict

        elif isinstance(item, list):
            for index, sub_item in enumerate(item):
                if isinstance(sub_item, (dict_item, list)):
                    item[index] = convert_json_to_object(sub_item)
                
            return item

class dict(dict_item): # https://goodcode.io/articles/python-dict-object/
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError(f'No such attribute: {name}')

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError(f'No such attribute: {name}')