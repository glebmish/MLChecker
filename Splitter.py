delimiters = ' \n\r\t'
detached = '.:,()\"\'[]{}/*+-^='


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def imp_split(delimiters, string, detached='', maxsplit=0):
    import re
    regex_pattern = '|'.join(map(re.escape, delimiters))

    pre_split = re.split(regex_pattern, string, maxsplit)
    ans_split = []

    for word in pre_split:
        word = word.replace('"""', '"')
        if is_number(word):
            ans_split.append(word)
            continue

        spl_words = []
        cur_word = ''

        for char in word:
            if char in detached:
                if cur_word != '':
                    spl_words.append(cur_word)

                spl_words.append(char)
                cur_word = ''

            else:
                cur_word += char

        if cur_word != '':
            spl_words.append(cur_word)

        ans_split += spl_words

    return ans_split


def detect_const(words):
    ans_new = []
    const_from = None

    for word in words:

        if const_from is not None:
            if const_from == "'" and word == "'" or \
                                    const_from == '"' and word == '"' or \
                                    const_from == '[' and word == ']' or \
                                    const_from == '{' and word == '}':
                ans_new.append('const')
                const_from = None

            else:
                continue

        elif is_number(word):
            ans_new.append('const')
        elif word == '"':
            const_from = '"'
        elif word == "'":
            const_from = "'"
        elif word == '[':
            const_from = '['
        elif word == '{':
            const_from = '{'
        else:
            ans_new.append(word)

    return ans_new
