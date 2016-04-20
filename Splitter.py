def imp_split(delimiters, string, detached='', maxsplit=0):
    import re
    regex_pattern = '|'.join(map(re.escape, delimiters))
    pre_split = re.split(regex_pattern, string, maxsplit)
    ans_split = []
    for word in pre_split:
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


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


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
            const_from = '}'
        else:
            ans_new.append(word)
    return ans_new


delimiters = ' \n\r\t'
detached = '.:,()\"\'[]{}'
string = 'for line in open(str): print line, \'abc\', "dsfs"\nreturn 0'
splitted = imp_split(delimiters, string, detached)
constanted = detect_const(splitted)
print string
print splitted
print constanted
