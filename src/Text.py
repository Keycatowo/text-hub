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

#%%
class Content:
    """
        Content為整篇文章的内容
        可以拆分成多個Paragraph
        支持不同的段落分割方式
            - 換行即為段落
            - 縮排為一個新的段落
            - 縮排為前一個段落的一部分
            - 使用openai的API來分割段落
    """
    def __init__(self, content, paragraph_split_method="openai"):
        self.content = re_replace(content) # 去除特殊符號
        self.paragraph_split_method = paragraph_split_method # 段落分割方法
        self.paragraph_list = self.split_paragraphs() # 段落列表
        
    def split_paragraphs(self):
        """
            拆分段落
        """
        if self.paragraph_split_method == "openai":
            return self.split_paragraphs_openai()
        elif self.paragraph_split_method == "line":
            return self.split_paragraphs_line()
        elif self.paragraph_split_method == "indent":
            return self.split_paragraphs_indent()
        elif self.paragraph_split_method == "anti-indent":
            return self.split_paragraphs_anti_indent()
        else
            raise ValueError("paragraph_split_method must be one of ['openai','line','indent','anti-indent']")
        
    def split_paragraphs_openai(self):
        """
            使用openai的API來分割段落
        """
        # 開發中，暫時不支持
        raise NotImplementedError("split_paragraphs_openai is not implemented yet")
    
    def split_paragraphs_line(self):
        """
            換行即為段落
        """
        # 拆分段落
        line_list = self.content.split("\n")
        # 去除每一行裡面的空白
        line_list = [line.strip() for line in line_list]
        # 去除空白行
        paragraph_list = [line for line in line_list if line != ""]
        return paragraph_list
        
        
    def split_paragraphs_indent(self):
        """
            縮排為一個新的段落
        """
        import re
        # 拆分段落
        line_list = self.content.split("\n")
        paragraph_list = []
        # 用一個迴圈來處理每行
        # 若該行為縮排，作為一個新的段落
        # 若該行不為縮排，則加入前一個段落
        paragraph_one = ""
        for line in line_list:
            # 若為縮排，則作為一個新的段落    
            if re.match(r"^\s+", line):
                paragraph_list.append(paragraph_one)
                paragraph_one = line.strip()
            else: # 若不為縮排，則加入前一個段落
                paragraph_one += line.strip()
        paragraph_list.append(paragraph_one)
        # 去除空白段落
        paragraph_list = [paragraph for paragraph in paragraph_list if paragraph != ""]
        return paragraph_list
                
            
    def split_paragraphs_anti_indent(self):
        """
            縮排為前一個段落的一部分
        """
        import re
        # 拆分段落
        line_list = self.content.split("\n")
        paragraph_list = []
        # 用一個迴圈來處理每行
        # 若該行為縮排，則加入前一個段落
        # 若該行不為縮排，作為一個新的段落
        paragraph_one = ""
        for line in line_list:
            
            # 若為縮排，則加入前一個段落
            if re.match(r"^\s+", line):
                paragraph_one += line.strip()
            else: # 若不為縮排，則作為一個新的段落
                paragraph_list.append(paragraph_one)
                paragraph_one = line.strip()
        paragraph_list.append(paragraph_one)
        # 去除空白段落
        paragraph_list = [paragraph for paragraph in paragraph_list if paragraph != ""]
        return paragraph_list
                
    

