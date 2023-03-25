"""
    測試劃分段落和劃分句子
"""
from texthub.Text import Content


def test_split_paragraphs_anti_indent():
    with open("example/anti-indent-paragraph.txt", "r", encoding="utf-8") as f:
        text = f.read()
    C = Content(text, paragraph_split_method="anti-indent")
    paragraph_list = C.split_paragraphs()
    assert len(paragraph_list) == 3
    assert paragraph_list[0] == "一、某人於某年某月某日，在某地某店購入某物品，包括某種空氣槍1支、CO2鋼瓶6瓶以及鋼珠52顆。儘管知道此類空氣槍屬於槍砲彈藥刀械管制條例管制的槍砲，未經中央主管機關許可，不得製造或持有，仍心懷製造殺傷力空氣槍的犯意。於某年某月某日，在某鎮某五金行購買彈簧並更換空氣槍上，增強其發射動能，製造出一支殺傷力空氣槍（槍枝管制編號1103011031）。從此以後，持有此空氣槍而未經許可。後於某年某月某日，警方在某處進行盤查時發現上述物品，當場扣押了具有殺傷力的空氣槍1支（槍枝管制編號1103011031）、CO2鋼瓶6瓶以及鋼珠52顆。該事件發生在彰化縣。"
    assert paragraph_list[1] == "二、某人於某年某月某日，在某地某店購入某物品，包括某種道具1個、藥品6包以及緊急救援設備52件。儘管知道此類道具及藥品具有某些危險性，使用時需特別小心，仍心懷使用不當的犯意。於某年某月某日，在某地點使用了上述物品，造成嚴重傷害。從此以後，違法持有上述物品。後於某年某月某日，警方在某處進行盤查時發現上述物品，當場扣押了上述物品。該事件發生在台北市。"
    assert paragraph_list[2] == "三、某人於某年某月某日，在某地某店購入某種化學品1桶、保護裝備6件以及實驗器具52件。儘管知道此類化學品屬於危險物質，使用時需特別小心，未經相關許"
    
    
