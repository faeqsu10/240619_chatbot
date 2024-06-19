import streamlit as st
from openai import OpenAI

st.title("친근한 챗봇")

# 사용자가 API 키를 입력할 수 있도록 텍스트 입력 박스 추가
api_key = st.text_input("OpenAI API 키를 입력해주세요", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    system_message = '''
    너의 이름은 친구봇이야.
    너는 항상 반말을 하는 챗봇이야. 다나까나 요 같은 높임말로 절대로 끝내지 마
    항상 반말로 친근하게 대답해줘.
    영어로 질문을 받아도 무조건 한글로 대답해줘.
    한글이 아닌 답변일 때는 다시 생각해서 꼭 한글로 만들어줘
    모든 답변 끝에 답변에 맞는 이모티콘도 추가해줘
    '''

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_message}]

    for message in st.session_state.messages:
        if message["role"] != "system":  # 시스템 메시지는 표시하지 않음
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("무슨 일이야?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.warning("API 키를 입력해주세요.")
