from typing import List


def split_pascal_case_string(s: str) -> List[str]:
    result = []
    current_word = s[0]

    for i in range(1, len(s)):
        if s[i].isupper():
            result.append(current_word)
            current_word = s[i]
        else:
            current_word += s[i]

    result.append(current_word)
    return result
