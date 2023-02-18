"""
    關於句子的模型封裝，支援train, predict, save, load等功能
"""

class Model:
    """
        關於句子的模型封裝，支援train, predict, save, load等功能
    """
    
    def __init__(self, model_name:str, label_list:list):
        self.model_name = model_name
        self.label_list = label_list

    def train(self, sentence_list:list, label_list:list):
        """
            sentence_list: 句子的list
            label_list: 每個句子的標籤
        """
        pass # TODO: 模型訓練
        

    def predict(self, sentence):
        """
            sentence可以是一個句子，也可以是一個句子的list
        """
        if isinstance(sentence, str):
            return self.predict_one(sentence)
        elif isinstance(sentence, list):
            return [self.predict_one(s) for s in sentence]
        else:
            raise Exception("sentence must be a string or a list of string")
        
    def save(self):
        pass

    def load(self):
        pass
    
    
    def predict_one(self, sentence):
        """
            預測一個句子的標籤
        """
        # 開發中，隨機返回一個標籤
        # TODO：實現模型預測
        import random
        return random.choice(self.label_list)