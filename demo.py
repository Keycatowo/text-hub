#%%
import streamlit as st
from src.Text import Content
from src.Model import Model

@st.experimental_memo
def convert_df(df):
    """
        Convert a pandas dataframe into a csv file.
        For the download button in streamlit.
    """
    return df.to_csv(index=False).encode('utf-8')

m1 = Model(model_name="Label1(A,B,C)", label_list=["A", "B", "C"])
m2 = Model(model_name="Label2(T,F)", label_list=["T", "F"])
st.write("範例模型1: ", m1.model_name, m1.label_list)
st.write("範例模型2: ", m2.model_name, m2.label_list)

with st.form("data_form"):
    text = st.text_area("輸入文字")
    paragraph_split_method = st.radio("段落分割方法", ["anti-indent","line", "indent"])
    sentence_split_method = st.radio("句子分割方法", ["length", "symbol"])
    paragraph_filter_regex = st.text_input("段落過濾正則表達式", value=r"(審酌).*")
    predicted = st.checkbox("預測", value=False)
    submit_button = st.form_submit_button(label="Submit")
    
if submit_button:
    content = Content(
        content=text,
        paragraph_split_method=paragraph_split_method,
        sentence_split_method=sentence_split_method,
        model_list=[m1, m2],
        paragraph_filter_regex=paragraph_filter_regex
    )
    if predicted:
        content.predict()
    st.write(content.df_sentence)
    
    # 提供下載
    st.download_button(
        label="下載",
        data=convert_df(content.df_sentence),
        file_name="sentence.csv",
    )