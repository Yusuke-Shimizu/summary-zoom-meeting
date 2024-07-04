import streamlit as st

# タイトルの設定
st.title('Streamlit サンプルアプリケーション')

# テキスト入力
user_input = st.text_input("名前を入力してください:")

# ボタン
if st.button('送信'):
    st.write(f'こんにちは、{user_input}さん！')

# スライダー
age = st.slider('年齢を選択してください:', 0, 100, 25)
st.write(f'あなたの年齢は {age} 歳です。')

# チェックボックス
if st.checkbox('データを表示する'):
    st.write('データを表示します。')

# セレクトボックス
option = st.selectbox(
    '好きな色を選んでください:',
    ['赤', '青', '緑']
)
st.write(f'あなたの好きな色は {option} です。')
