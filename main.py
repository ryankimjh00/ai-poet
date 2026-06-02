import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import streamlit as st

load_dotenv()

STUDENT_ID = "2191298"


def get_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    try:
        return st.secrets.get("OPENAI_API_KEY", api_key)
    except Exception:
        return api_key


st.set_page_config(page_title=f"AI Poet {STUDENT_ID}", page_icon="✍️")
st.title("인공지능 시인")
st.caption(f"학번: {STUDENT_ID}")

subject = st.text_input("시의 주제를 입력해주세요.", placeholder="예: 봄비, 우주, 커피")
style = st.selectbox("시의 분위기를 선택해주세요.", ["서정적인", "따뜻한", "희망찬", "재미있는", "잔잔한"])
line_count = st.slider("시의 줄 수", min_value=4, max_value=12, value=8, step=2)

if st.button("시 작성", type="primary"):
    subject = subject.strip()
    if not subject:
        st.warning("시의 주제를 입력해주세요.")
        st.stop()

    api_key = get_openai_api_key()
    if not api_key:
        st.error("OPENAI_API_KEY를 Streamlit Secrets에 등록해주세요.")
        st.stop()

    chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.8, api_key=api_key)
    prompt = (
        f"'{subject}'을 주제로 {style} 분위기의 한국어 시를 {line_count}줄로 써줘. "
        "제목을 먼저 쓰고, 이후 시 본문만 간결하게 작성해줘."
    )
    with st.spinner("시 작성중 ..."):
        result = chat_model.invoke(prompt)
    st.markdown(result.content)
