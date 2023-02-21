"""


"""
import pandas as pd

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
        Content為整篇文章的内容，一個Content會具有以下屬性：
            - content: 文章的內容
            - paragraph_split_method: 段落分割方法
            - title: 文章的標題
            - text_ID: 文章的ID
            - df_sentence: 文章的句子列表
                - paragraph_ID: 段落編號
                - sentence_ID: 句子編號
                - sentence: 句子內容
                - label1: 句子的第一個標籤
                - label2: 句子的第二個標籤
                - ...
        可以拆分成多個Paragraph
        支持不同的段落分割方式
            - 換行即為段落
            - 縮排為一個新的段落
            - 縮排為前一個段落的一部分
            - 使用openai的API來分割段落
    """
    def __init__(self, content, paragraph_split_method="line", title="Content", text_ID=None, **kwargs): # 支援往下傳遞的參數
        #* 檢查參數
        if not content:
            raise ValueError("The 'content' parameter cannot be empty.")
        if not isinstance(content, str):
            raise TypeError("The 'content' parameter must be a string.")
        
        #* 參數設定 
        self.paragraph_split_method = paragraph_split_method # 段落分割方法
        self.title = title # 文章的標題
        # 如果沒有指定ID，則使用文章的內容的MD5值作為ID
        if text_ID is None:
            import hashlib
            self.text_ID = hashlib.md5(content.encode("utf-8")).hexdigest()
        else:
            self.text_ID = text_ID
        
        #* 初始化
        self.content = re_replace(content) # 前處理去除特殊符號
        paragraph_list = self.split_paragraphs() # 段落列表
        # 將每個段落轉換成Paragraph類型的物件，加上段落編號為ID
        self.Paragraph_list = [Paragraph(paragraph, paragraph_ID=i, **kwargs) for i, paragraph in enumerate(paragraph_list)]
        #// self.Paragraph_list = [Paragraph(paragraph, **kwargs) for paragraph in paragraph_list]
        
        #* 初始化df_sentence
        # 將每個段落的df_sentence合併成一個大的df_sentence, 並加上段落ID
        df_sentence_list = [P.df_sentence.assign(paragraph_ID=P.paragraph_ID) for P in self.Paragraph_list]
        self.df_sentence = pd.concat(df_sentence_list, ignore_index=True)
        # 重設column順序，paragraph_ID放在最前面、sentence_ID放在第二個、sentence放在第三個
        self.df_sentence = self.df_sentence[["paragraph_ID","sentence_ID","sentence"] + [col for col in self.df_sentence.columns if col not in ["paragraph_ID","sentence_ID","sentence"]]]
        
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
        Paragraph為文章的一個段落，一個Paragraph會包含以下資訊
            - paragraph: 段落的內容
            - sentence_split_method: 句子分割方法
            - paragraph_ID: 段落的ID
            - df_sentence: 句子的DataFrame，包含以下欄位
                - sentence_ID: 句子的ID
                - sentence: 句子的內容
                - label1: 句子的第一個標籤
                - label2: 句子的第二個標籤
                - ...
        可以拆分成多個Sentence
        支持不同句子分割方式
            - 使用符號分割，如句號、問號、感嘆號
            - 使用長度分割，如每個句子長度不超過20個字
            - 使用openai的API來分割段落
    """
    def __init__(self, paragraph, sentence_split_method="length", paragraph_ID=0, **kwargs):
        #* 檢查參數
        if not isinstance(paragraph, str):
            raise TypeError("paragraph must be a string")
        if not isinstance(paragraph_ID, int):
            raise TypeError("paragraph_ID must be an integer")
        
        #* 初始化
        self.paragraph = paragraph
        self.sentence_split_method = sentence_split_method
        self.paragraph_ID = paragraph_ID
        sentence_list = self.split_sentences()
        
        #* 初始化Sentence
        # 將每個句子轉換成Sentence類型的物件，加上句子編號為ID
        self.Sentence_list = [Sentence(sentence, sentence_ID=i, **kwargs) for i, sentence in enumerate(sentence_list)]
        
        #* 初始化df_sentence
        model_list = kwargs.get("model_list", [])
        model_name_list = [model.model_name for model in model_list]
        self.df_sentence = pd.DataFrame(
            columns = ["sentence_ID", "sentence"] + model_name_list
        )
        self.df_sentence["sentence_ID"] = [S.sentence_ID for S in self.Sentence_list]
        self.df_sentence["sentence"] = [S.sentence for S in self.Sentence_list]
        for model_name in model_name_list:
            self.df_sentence[model_name] = [S.tags[model_name] for S in self.Sentence_list]
        
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
    def __init__(self, sentence, sentence_ID=0, model_list=[]):
        #* 檢查參數
        if not isinstance(sentence, str):
            raise TypeError("sentence must be a string")
        if not isinstance(sentence_ID, int):
            raise TypeError("sentence_ID must be an integer")
        
        #* 初始化
        self.sentence = sentence
        self.sentence_ID = sentence_ID
        self.model_list = model_list
        self.tags = {}
        for model in model_list:
            self.tags[model.model_name] = None
        
    
    def predict(self):
        """
            使用不同的模型來預測句子的tag
        """
        for model in self.model_list:
            self.tags[model.model_name] = model.predict(self.sentence)
    