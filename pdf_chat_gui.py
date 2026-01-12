'''
논문(PDF)를 업로드하고, 내용 요약 및 질의.
데모 페이지.
'''
import os
import time
import tempfile
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# 페이지 기본 설정
st.set_page_config(
    page_title="PDF 요약 및 Q&A 봇",
    page_icon="📄",
    layout="wide"
)

# 환경 변수 로드
load_dotenv()

# 사이드바 설정
with st.sidebar:
    st.title("⚙️ 설정")
    api_key_env = os.getenv("GOOGLE_API_KEY")
    api_key = st.text_input("Google API Key", value=api_key_env if api_key_env else "", type="password")
    
    st.divider()
    
    uploaded_file = st.file_uploader("PDF 파일 업로드", type=["pdf"])
    
    st.info("💡 파일을 업로드하면 자동으로 Gemini에 전송되어 처리됩니다.")

# 메인 화면
st.title("📄 문서 요약 및 대화하기")

if not api_key:
    st.warning("Google API Key를 입력해 주세요.")
    st.stop()

# API 설정
genai.configure(api_key=api_key)

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "gemini_file" not in st.session_state:
    st.session_state.gemini_file = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "last_uploaded_filename" not in st.session_state:
    st.session_state.last_uploaded_filename = None

def process_file(uploaded_file):
    """파일을 업로드하고 처리가 완료될 때까지 기다립니다."""
    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    with st.spinner(f"파일 업로드 중... ({uploaded_file.name})"):
        # 파일을 Gemini에 업로드
        sample_file = genai.upload_file(path=tmp_path, display_name=uploaded_file.name)
        
        # 처리 상태 확인
        while sample_file.state.name == "PROCESSING":
            time.sleep(2)
            sample_file = genai.get_file(sample_file.name)
        
        if sample_file.state.name == "FAILED":
            st.error("파일 처리에 실패했습니다.")
            os.remove(tmp_path)
            return None
            
    # 로컬 임시 파일 삭제
    os.remove(tmp_path)
    return sample_file

# 파일이 새로 업로드되었거나 변경되었을 때 처리
if uploaded_file and (st.session_state.last_uploaded_filename != uploaded_file.name):
    st.session_state.gemini_file = process_file(uploaded_file)
    st.session_state.last_uploaded_filename = uploaded_file.name
    st.session_state.chat_history = [] # 새 파일이면 대화 기록 초기화
    st.session_state.summary = None # 새 파일이면 요약 초기화

# 파일이 준비되었을 때 표시되는 UI
if st.session_state.gemini_file:
    # 탭 생성 (요약 vs 채팅)
    tab1, tab2 = st.tabs(["📑 요약 보기", "💬 문서와 대화하기"])

    # 모델 초기화
    model = genai.GenerativeModel('gemini-3-flash-preview')

    with tab1:
        if st.session_state.summary:
            st.markdown(st.session_state.summary)
        else:
            if st.button("📝 이 문서 요약하기", type="primary"):
                with st.spinner("요약 생성 중..."):
                    try:
                        response = model.generate_content([st.session_state.gemini_file, "이 문서를 한국어로 상세하게 요약해 주세요."])
                        st.session_state.summary = response.text
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"요약 생성 중 오류 발생: {e}")

    with tab2:
        # 채팅 기록 표시
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 사용자 입력
        if prompt := st.chat_input("문서에 대해 질문해 보세요"):
            # 사용자 메시지 표시
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            # 모델 응답 생성
            with st.chat_message("assistant"):
                with st.spinner("답변 생성 중..."):
                    try:
                        # 대화 맥락 구성 (멀티모달)
                        # 단순한 방식: 매번 파일과 질문을 함께 던지거나, ChatSession 사용
                        # 여기서는 ChatSession을 사용하되 history 관리를 직접 제어
                        
                        # 히스토리 포맷 변환 (Gemini SDK 형식)
                        history_for_gemini = []
                        # 첫 메시지에 파일 컨텍스트 추가 (시스템 프롬프트 역할)
                        history_for_gemini.append({
                            "role": "user",
                            "parts": [st.session_state.gemini_file, "이 문서를 기반으로 대화를 나눌 것입니다."]
                        })
                        history_for_gemini.append({
                            "role": "model",
                            "parts": ["네, 알겠습니다. 문서에 대해 무엇이든 물어보세요."]
                        })

                        # 이전 대화 내용 추가
                        for msg in st.session_state.chat_history[:-1]: # 마지막 질문 제외
                            role = "user" if msg["role"] == "user" else "model"
                            history_for_gemini.append({
                                "role": role,
                                "parts": [msg["content"]]
                            })
                        
                        # 채팅 세션 시작 및 메시지 전송
                        chat = model.start_chat(history=history_for_gemini)
                        response = chat.send_message(prompt)
                        
                        st.markdown(response.text)
                        
                        # 어시스턴트 메시지 저장
                        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                        
                    except Exception as e:
                        st.error(f"답변 생성 중 오류 발생: {e}")

else:
    # 파일이 없을 때 초기 화면
    st.markdown("""
    ### 👋 환영합니다!
    
    왼쪽 사이드바에서 **PDF 문서**를 업로드하면:
    1. 문서의 내용을 자동으로 **요약**해 줍니다.
    2. 챗봇과 대화하며 문서 내용에 대해 **질의응답**을 할 수 있습니다.
    
    지금 바로 시작해 보세요! 🚀
    """)
