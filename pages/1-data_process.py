"""
    資料處理：將原始文字資料進行斷句後轉換成表格資料
"""
import streamlit as st
from texthub.Text import Content
from io import StringIO
import pandas as pd

st.title("資料處理")
st.write("將原始文字資料進行斷句後轉換成表格資料")

@st.cache_data 
def convert_df(df):
    """
        Convert a pandas dataframe into a csv file.
        For the download button in streamlit.
    """
    return df.to_csv(index=False).encode('utf-8_sig')


# 顯示上傳資料的區塊
with st.expander("上傳原始資料"):
    # 允許使用者上傳多個檔案
    uploaded_files = st.file_uploader("上傳多個檔案", accept_multiple_files=True)

    # 如果有檔案上傳
    if uploaded_files:
        content_list = []
        st.write("已上傳以下檔案:")
        for uploaded_file in uploaded_files:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            file_contents = uploaded_file.read()
            content_list.append(string_data)
            st.write("- ", uploaded_file.name, ":", len(file_contents), "bytes")

# 資料處理的區塊

# 建立一個參數的map table
parameter_map = {
    # 段落分割方法
    "縮排為前行同一段": "anti-indent",
    "每行都為一段": "line",
    "縮排為新的一段": "indent",
    "不分段": "none",
    
    # 句子分割方法
    "只依符號斷句": "symbol",
    "只依長度斷句": "length",
    "依符號與長度斷句": "length+symbol",
    "使用模型斷句": "model"
}
if uploaded_files:
    with st.expander("資料處理設定"):
        # 是否開啟高級設定
        advanced_settings = st.checkbox("開啟高級設定(允許使用正則表達式過濾段落或句子)")
        
        paragraph_split_method = st.radio("段落分割方法", ["縮排為前行同一段", "每行都為一段", "縮排為新的一段", "不分段"])
        paragraph_filter_regex = st.text_input("段落過濾正則表達式", value=r"(審酌).*") if advanced_settings else None
        sentence_split_method = st.radio("句子分割方法", ["只依符號斷句", "只依長度斷句", "依符號與長度斷句", "使用模型斷句"])
        sentence_filter_regex = st.text_input("句子過濾正則表達式", value=r"(審酌).*") if advanced_settings else None
        
        # 要預期的欄位名稱
        properties = st.text_input("請輸入建立預測欄位名稱，並以逗號分隔(不要有空格)，例如：`預測類別1,預測類別2`", value="")
        # 將欄位名稱轉換成list
        properties_list = properties.split(",") if properties else []
        st.write("預測類別對照表", properties_list)
        
        
        # # 資料處理範例
        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     st.write("原始資料")
        #     # 選擇哪一個檔案
        #     file_index = st.selectbox("選擇檔案", list(range(len(uploaded_files))))
        #     # 顯示原始資料
        #     st.write("原始資料", uploaded_files[file_index].read().decode("utf-8"))
    C_list = [
        Content(
            content=content,
            paragraph_split_method=parameter_map[paragraph_split_method],
            paragraph_filter_regex=paragraph_filter_regex,
            sentence_split_method=parameter_map[sentence_split_method],
            # sentence_filter_regex=sentence_filter_regex,
        )
        for content in content_list
    ]
    
    with st.expander("資料處理個別檢視"):
        for C, uploaded_file in zip(C_list, uploaded_files):
            st.write(f"檔案名稱：{uploaded_file.name}")
            st.write(f"文件ID: {C.text_ID}")
            st.write(C.df_sentence)    

    for C in C_list:
        C.df_sentence["TextID"] = C.text_ID
        # 重新排列欄位，TextID為第一個欄位
        C.df_sentence = C.df_sentence[["TextID"] + [col for col in C.df_sentence.columns if col != "TextID"]]
        for property in properties_list:
            C.df_sentence[property] = ""

    # 合併所有的資料提供下載
    df_all = pd.concat([C.df_sentence for C in C_list])
    st.download_button(
        label="下載斷句資料",
        data=convert_df(df_all),
        file_name="斷句資料.csv"
    )
