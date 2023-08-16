import uuid

class RegisteredApiFormat:
    method: str
    func: callable

    def __init__(self, method: str, func: callable):
        self.method = method
        self.func = func

class GetDictFromClass:
    def get_dict_from_class(self, class_obj):
        new_dict = dict()
        class_obj_vars = vars(class_obj)
        keys = list(class_obj_vars.keys())
        for key in keys:
            if not key.startswith("__"):
                value = class_obj_vars.get(key)
                new_dict[key] = self.get_single_value(key, value)
        return new_dict

    def get_single_value(self, key, value):
        return value

class GetSlugDict(GetDictFromClass):
    def get_single_value(self, key, value):
        return {
            "method": value.method,
            "func": value.func,
            "slug": key
        }


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False