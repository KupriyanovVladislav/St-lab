def get_max_and_min(data: typing.Set[typing.Union[decimal.Decimal,
                                                  fractions.Fraction, str]])\
        -> typing.NamedTuple:
    for num in data:
        if isinstance(num, str):
            if " \ " in num:
                str_repr = num.replace(' \ ', '/')
                data.add(fractions.Fraction(str_repr))
            else:
                data.add(decimal.Decimal(num))
            data.remove(num)
    CustomTuple = collections.namedtuple('CustomTuple',
                                         ['max_value', 'min_value'])
    return CustomTuple(max_value=max(data), min_value=min(data))
