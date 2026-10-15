Python 공식 슬림 이미지 사용

FROM python:3.10-slim

작업 디렉토리 설정

WORKDIR /app

필수 라이브러리 목록 복사 및 설치

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

애플리케이션 소스 코드 복사

COPY main.py .

환경 변수 설정 (포트 지정)

ENV PORT=8080

Gunicorn을 사용하여 Flask 앱 실행 (프로덕션 환경 최적화)

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app", "--workers", "1", "--threads", "8", "--timeout", "0"]
