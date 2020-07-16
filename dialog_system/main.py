from dialog_system.config import MESSAGES

import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# constants
re_char = re.compile("[\w,\s,\d]")
text = "Пока!asdf 324xf"


def normalize_phrase(string: str):
    new_string = ""
    string = string.lower()
    for c in string:
        if is_char(c):
            new_string += c
    return new_string


def is_char(char: str):
    return not not re_char.findall(char)


def comparison_string(string: str):
    normal_string = normalize_phrase(string)
    max_pair = {
        "word": None,
        "answers": [],
        "value": 0,
    }
    for container in MESSAGES['cases']:
        tmp_value = 0
        tmp_word = None
        for phrase in container["phrases"]:
            tmp = fuzz.ratio(normal_string, normalize_phrase(phrase))
            if tmp > tmp_value:
                tmp_word = phrase
                tmp_value = tmp

        if tmp_value > max_pair["value"]:
            max_pair["value"] = tmp_value
            max_pair["answers"] = container["reaction"]
            max_pair["word"] = tmp_word

    return max_pair


def get_answer(string: str, limit: int = 40):
    result = {
        "success": False,
        "answers": []
    }
    pair = comparison_string(string)
    if pair["value"] <= limit:
        return result

    result["success"] = True
    result["answers"] = pair["answers"]

    return result


if __name__ == '__main__':
    print(get_answer(text, 43))
