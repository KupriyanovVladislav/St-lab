def analyze_students(data: typing.Dict[str, typing.Dict]) -> typing.Set[typing.Tuple]:
    return {(name, subject, functools.reduce(lambda x, y: x * y, data[name][subject])) for name in data for subject in data[name] if not subject == "1C"}


def validate_data(data: typing.Dict[str, typing.Dict]) -> bool:
    for name in data:
        if not isinstance(name, str):
            raise TypeError
        for let in name:
            if not (ord("a") <= ord(let.lower()) <= ord("z") or
                    ord("0") <= ord(let) <= ord("9")):
                raise ValueError

        for subject in data[name]:
            if not isinstance(subject, str):
                raise TypeError
            for let in subject:
                if not (ord("a") <= ord(let.lower()) <= ord("z") or
                        ord("0") <= ord(let) <= ord("9")):
                    raise ValueError

            for mark in data[name][subject]:
                if not isinstance(mark, int) or isinstance(mark, bool):
                    raise TypeError
                elif not 1 <= mark <= 10:
                    raise ValueError
    return True