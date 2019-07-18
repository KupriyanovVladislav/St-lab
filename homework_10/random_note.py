from collections import Counter


def checkMagazine(magazine: list[str], note: list[str]) -> None:
    main_words = Counter(magazine)
    secondary_words = Counter(note)
    for key in secondary_words.keys():
        if not(key in magazine and secondary_words.get(key) <= main_words.get(key)):
            print("No")
            break
    else:
        print("Yes")
