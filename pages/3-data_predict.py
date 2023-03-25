import streamlit as st
from texthub.Model import Model

st.title("模型預測")

with st.expander("上傳斷句檔案"):

    # 支援上傳斷句後的csv檔
    uploaded_file = st.file_uploader("請上傳斷句後的csv檔", type="csv")
    if uploaded_file:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        df = df.fillna("")
        df = df[df["sentence"] != ""]
        st.write(df)
        st.write("上傳成功")
    


if uploaded_file:
    with st.form("模型選擇"):
        model_name = st.text_input("請輸入模型名稱", value="IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment")
        tokenizer_name = st.text_input("請輸入tokenizer名稱", value="IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment")
        model_submit = st.form_submit_button("確認")
    if model_submit:
        model = Model(model_name=model_name, tokenizer_name=tokenizer_name)
        st.write(model.label_list)
        
        df["predict"] = df["sentence"].apply(model.predict)
        df["senti"] = df["predict"].apply(lambda x: x[0]["label"])
        df["score"] = df["predict"].apply(lambda x: x[0]["score"])
        
        st.write(df)