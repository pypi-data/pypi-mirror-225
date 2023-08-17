class convert_json_to_object:
    def __new__(self, item):
        if isinstance(item, dict):
            updated_dict = _convert_dictionary_to_object()
            for key, value in item.items():
                if isinstance(value, (dict, list)):
                    value = convert_json_to_object(value)
                setattr(updated_dict, key, value)
                    
            return updated_dict

        elif isinstance(item, list):
            for index, sub_item in enumerate(item):
                if isinstance(sub_item, (dict, list)):
                    item[index] = convert_json_to_object(sub_item)
                
            return item

class _convert_dictionary_to_object(dict): # https://goodcode.io/articles/python-dict-object/
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)