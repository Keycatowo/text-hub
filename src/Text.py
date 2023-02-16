"""


"""
RE_TABLE = {
    ".": "<re_dot>",
    "^": "<re_head>",
    "$": "<re_dollor>",
    "*": "<re_star>",
    "+": "<re_plus>",
    "?": "<re_question>",
    "{": "<re_bracket_L3>",
    "}": "<re_bracket_R3>",
    "[": "<re_bracket_L2>",
    "]": "<re_bracket_R2>",
    "(": "<re_bracket_L1>",
    ")": "<re_bracket_R1>",
    "|": "<re_or>",
    "&": "<re_and>",
    ":": "<re_colon>",
    "=": "<re_equal>",
    "-": "<re_minus>",
}

def re_replace(text,inverse=False):
    from bidict import bidict
    # 選擇取代表
    if inverse == False:
        re_table = RE_TABLE
    else:
        re_table = dict(bidict(RE_TABLE).inverse)

    # 取代所有元素
    for key in re_table.keys():
        text = text.replace(key, re_table[key])
    return text

