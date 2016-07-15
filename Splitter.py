import re


def detect_const(text):
    regex_pattern = r'(\[.*?\])|(\{.*?\})|(\'.*?\')|(""".*?""")|(".*?")|(\d+\.\d+)|(\d+)'
    return re.sub(regex_pattern, '_CONST', text)


def imp_split(text):
    regex_pattern = r'(\.|:|;|,|\(|\)|"|\'|\[|\]|\{|\}|/|\*|\+|\-|\^|=|\s)\s*'
    return [word for word in re.split(regex_pattern, text) if word not in ' \r\t']
