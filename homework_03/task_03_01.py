import re


class RegParser:
    ADDRESS_REGEX = r"^(?:[A-Z][a-z]+, )?(?:[A-Z][a-z]+(?: City| city)?, )?" \
                    r"(?:(?:[\w _-]+)(?: str[\.])?, ){1}(?:\d+(?: *[-,\\|/] *)\d+){1}$"
    CONTACT_REGEX = r"^(?:(?:name=(?P<name>[-\w ]*)|surname=(?P<surname>[-\w ]*)|" \
                    r"age=(?P<age>[-\w ]*)|city=(?P<city>[-\w ]*))(?:;|$)){1,4}(?<!;)$"
    PRICE_REGEX = r'(?<=[\$€] )\d+(?:[\.,]\d+)?|\d+(?:[\.,]\d+)?(?= *BYN)'

    @classmethod
    def find(cls, text: str, choise: int):
        if choise == 1:
            return re.findall(cls.ADDRESS_REGEX, text, flags=re.MULTILINE)
        result_match = []
        if choise == 2:
            splited_text = text.split(sep='\n')
            for string in splited_text:
                try:
                    matches = re.match(cls.CONTACT_REGEX, string).groupdict()
                    result_match.append({key: matches[key] for key in matches.keys() if matches[key]})
                except AttributeError:
                    continue
        elif choise == 3:
            nums = re.findall(cls.PRICE_REGEX, text, flags=re.MULTILINE)
            for num in nums:
                if "," in num or "." in num:
                    result_match.append(float(num.replace(',', '.')))
                else:
                    result_match.append(int(num))
        return result_match
