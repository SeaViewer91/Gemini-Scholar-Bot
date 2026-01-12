Gemini 3.0 PDF 요약 및 질의응답 시스템

Gemini 3.0 API와 Streamlit을 활용하여 PDF 문서의 내용을 분석, 요약하고 대화형 질의응답을 수행하는 프로그램임.

1. 주요 기능

PDF 텍스트 분석: 업로드된 PDF 파일을 Gemini File API를 통해 서버 측에서 직접 처리함.

자동 요약: 문서 업로드와 동시에 Gemini 모델이 전체 내용을 파악하여 핵심 요약본을 생성함.

문맥 유지 대화: 세션 상태(Session State)를 활용하여 이전 대화 기록을 포함한 연속성 있는 질의응답을 지원함.

실시간 스트리밍: Streamlit 인터페이스를 통해 처리 과정 및 답변을 실시간으로 확인 가능함.

2. 기술 스택

Language: Python 3.9+

Framework: Streamlit

LLM API: Google Gemini 3.0 (gemini-2.0-flash-exp 등)

Environment: python-dotenv (환경 변수 관리)

3. 설치 및 설정

3.1. 의존성 설치

저장소를 클론한 후 필요한 라이브러리를 설치함.

pip install -r requirements.txt


3.2. 환경 변수 설정

프로젝트 루트 디렉토리에 .env 파일을 생성하고 Google AI Studio에서 발급받은 API 키를 입력함.

GOOGLE_API_KEY=your_api_key_here


4. 실행 방법

4.1. 모델 확인 (선택 사항)

현재 API 키로 접근 가능한 모델 리스트 확인용 스크립트를 실행함.

python check_models.py


4.2. 애플리케이션 실행

Streamlit 서버를 구동하여 웹 인터페이스를 실행함.

streamlit run pdf_chat_gui.py


5. 프로젝트 구조

pdf_chat_gui.py: 메인 애플리케이션 파일. UI 구성 및 Gemini API 연동 로직 포함.

check_models.py: API 연결 테스트 및 지원 모델 확인용 유틸리티.

requirements.txt: 실행에 필요한 의존성 패키지 목록.

.env: API 키 등 보안 정보 관리 파일 (Git 포함 주의).

6. 주의 사항

API 사용량: 무료 티어 사용 시 호출 횟수 제한(Rate Limit)에 따른 오류 발생 가능성 있음.

보안: .env 파일이 외부 저장소에 노출되지 않도록 .gitignore 설정 권장함.

파일 크기: Gemini File API 제한 사항에 따라 대용량 PDF 처리가 제한(2GB 이내)될 수 있음.
