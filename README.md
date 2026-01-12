# 논문(PDF) 요약 및 질의응답 데모

Google Gemini API를 활용하여 업로드된 PDF 논문을 요약하고, 해당 논문 내용을 바탕으로 질의응답(Q&A)을 수행하는 데모 프로그램이다. Streamlit 프레임워크를 기반으로 웹 인터페이스를 제공한다.

## 구성 파일 설명

본 프로젝트는 다음 4개의 파일로 구성된다.

1.  **`pdf_chat_gui.py`**
    *   메인 애플리케이션 파일이다.
    *   Streamlit을 사용하여 PDF 파일 업로드, 논문 요약, 채팅 인터페이스를 제공한다.
    *   업로드된 파일을 Gemini에 전송하고, `gemini-3-flash-preview` 모델을 사용하여 요약 및 대화를 수행한다.

2.  **`check_models.py`**
    *   사용 가능한 Google Gemini 모델 목록을 확인하는 유틸리티 스크립트이다.
    *   API 키 설정 상태를 확인하고, `generateContent` 메서드를 지원하는 모델명을 출력한다.

3.  **`requirements.txt`**
    *   프로그램 실행에 필요한 Python 라이브러리 목록이 기재되어 있다.
    *   주요 의존성: `streamlit`, `google-generativeai`, `python-dotenv`.

4.  **`.env`**
    *   환경 변수 설정 파일이다.
    *   Google API Key (`GOOGLE_API_KEY`)를 저장하여 코드 내에서 호출할 수 있게 한다.

## 설치 방법

Python 환경(3.9 이상 권장)에서 다음 명령어를 통해 필요한 패키지를 설치한다.

```bash
pip install -r requirements.txt
```

## 설정

`check_models.py` 및 `pdf_chat_gui.py` 실행을 위해서는 유효한 Google API Key가 필요하다. `.env` 파일을 생성하거나 수정하여 키를 입력한다.

```env
GOOGLE_API_KEY=your_api_key_here
```

## 실행 방법

### 1. 모델 확인 (선택 사항)
사용 가능한 모델 목록을 확인하려면 다음 명령어를 실행한다.

```bash
python check_models.py
```

### 2. 프로그램 실행 (GUI)
웹 인터페이스를 실행하려면 Streamlit 명령어를 사용한다.

```bash
streamlit run pdf_chat_gui.py
```

실행 후 브라우저가 자동으로 열리며, 열리지 않을 경우 터미널에 표시된 로컬 URL(예: `http://localhost:8501`)로 접속한다.

## 주요 기능

*   **PDF 업로드**: 사이드바를 통해 PDF 파일을 업로드할 수 있다.
*   **자동 요약**: 업로드된 문서의 내용을 자동으로 요약하여 제공한다.
*   **문서 기반 대화**: 챗봇 인터페이스를 통해 문서 내용에 대해 질문하고 답변을 받을 수 있다.
*   **멀티모달 처리**: 문서를 텍스트로 변환하지 않고 파일 자체를 모델에 전달하여 처리한다.
