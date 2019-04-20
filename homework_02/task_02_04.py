import types


def pep8_warrior(future_class_name, future_class_parents, future_class_attr):
    attrs = ((name, value) for name, value in future_class_attr.items())
    new_dict = dict()
    print(attrs)
    for name, value in attrs:
        if isinstance(value, types.FunctionType) and name[0] != '__':
            new_dict.update({name.lower(): value})
        elif isinstance(value, type):
            name = name.title()
            name = name.replace("_", "")
            new_dict.update({name: value})
        else:
            new_dict.update({name.upper(): value})
    return type(future_class_name, future_class_parents, new_dict)


class Pep8Warrior(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items())
        new_dict = dict()
        for name, value in attrs:
            if isinstance(value, types.FunctionType) and name[0] != '__':
                new_dict.update({name.lower(): value})
            elif isinstance(value, type):
                name = name.title()
                name = name.replace("_", "")
                new_dict.update({name: value})
            else:
                new_dict.update({name.upper(): value})
        return type.__new__(cls, name, bases, new_dict)
