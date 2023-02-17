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
    def __init__(self, content, paragraph_split_method="line", **kwargs): # 支援往下傳遞的參數
        # 檢查參數
        if not content:
            raise ValueError("The 'content' parameter cannot be empty.")
        
        # 參數設定
        self.paragraph_split_method = paragraph_split_method # 段落分割方法
        self.kwargs = kwargs.items() # 支援往下傳遞的參數
        
        self.content = re_replace(content) # 前處理去除特殊符號
        paragraph_list = self.split_paragraphs() # 段落列表
        # 將每個段落轉換成Paragraph類型的物件
        self.Paragraph_list = [Paragraph(paragraph, **kwargs) for paragraph in paragraph_list]
        
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
        else:
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
        paragraph_buffer = ""
        for line in line_list:
            
            # 若為縮排，則加入前一個段落
            if re.match(r"^\s+", line):
                paragraph_buffer += line.strip()
            else: # 若不為縮排，則作為一個新的段落
                paragraph_list.append(paragraph_buffer)
                paragraph_buffer = line.strip()
        paragraph_list.append(paragraph_buffer) # 最後一個段落
        # 去除空白段落
        paragraph_list = [paragraph for paragraph in paragraph_list if paragraph != ""]
        return paragraph_list
                
    


class Paragraph:
    """
        Paragraph為文章的一個段落
        可以拆分成多個Sentence
        支持不同句子分割方式
            - 使用符號分割，如句號、問號、感嘆號
            - 使用長度分割，如每個句子長度不超過20個字
            - 使用openai的API來分割段落
    """
    def __init__(self, paragraph, sentence_split_method="length", **kwargs):
        self.paragraph = re_replace(paragraph)
        self.sentence_split_method = sentence_split_method
        self.sentence_list = self.split_sentences()
        
    def split_sentences(self):
        """
            拆分句子
        """
        if self.sentence_split_method == "openai":
            return self.split_sentences_openai()
        elif self.sentence_split_method == "symbol":
            return self.split_sentences_symbol()
        elif self.sentence_split_method == "length":
            return self.split_sentences_length()
        else:
            raise ValueError("sentence_split_method must be one of ['openai','symbol','length']")
        
    def split_sentences_openai(self):
        """
            使用openai的API來分割句子
        """
        # 開發中，暫時不支持
        raise NotImplementedError("split_sentences_openai is not implemented yet")
    
    def split_sentences_symbol(self):
        """
            使用符號優先分割句子
        """
        import re
        # 拆分句子
        sentence_list = re.split(r"([。？！])", self.paragraph) # 用符號分割句子
        sentence_list = ["".join(sentence_list[i:i+2]) for i in range(0, len(sentence_list), 2)] # 每2個元素為一個句子，保留符號
        # 去除每一句裡面的空白
        sentence_list = [sentence.strip() for sentence in sentence_list]
        # 去除空白句子
        sentence_list = [sentence for sentence in sentence_list if sentence != ""]
        return sentence_list
    
    def split_sentences_length(self, max_length=50):
        """
            使用長度優先分割句子
        """
        import re
        # 用任何符號分割句子
        sub_sentence_list = re.split(r"([。？！、；,」\.])", self.paragraph)
        # 將不超過max_length的句子合併
        sentence_list = []
        sub_sentence_buffer = "" 
        for sub_sentence in sub_sentence_list:
            # 若句子長度不超過max_length，則加入前一個句子
            if len(sub_sentence_buffer) + len(sub_sentence) <= max_length:
                sub_sentence_buffer += sub_sentence
            else: # 若句子長度超過max_length，則作為一個新的句子
                sentence_list.append(sub_sentence_buffer)
                sub_sentence_buffer = sub_sentence
        sentence_list.append(sub_sentence_buffer) # 最後一個句子
        return sentence_list
    

class Sentence:
    """
        Sentence為段落的一個句子，在目前系統中為最小單位
        每個句子會針對不同的判斷模型，有不同的tag
    """
    def __init__(self, sentence):
        self.sentence = re_replace(sentence)
        self.tags = {}
        
    