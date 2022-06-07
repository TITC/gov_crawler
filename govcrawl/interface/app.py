import streamlit as st
from govcrawl.analysis import postprocess
import pandas as pd
import numpy as np

st.title('词频统计')

st.markdown("### 请选择城市")

city_name = st.selectbox(label="城市", options=('武汉', '芜湖', '合肥'))

city_name = {'武汉': 'wuhan', '芜湖': 'wuhu', '合肥': 'hefei'}[city_name]

st.write('You selected:', city_name)
st.markdown("### 请输入待查询词汇")
txt = st.text_area('待查询词汇(多个词用中文逗号分割)', '''疫情''')
wordsfreq = [(word, postprocess(city_name=city_name).get(word, 0)) for word in txt.split("，")]


df = pd.DataFrame(
    wordsfreq,
    columns=("搜索词", "频次"))
st.table(df)
