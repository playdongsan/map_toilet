# 베이스 이미지 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# 애플리케이션 파일 복사
COPY . .

# 환경 변수 설정
ENV PORT 8000

# 애플리케이션 실행
CMD ["python", "main.py"]
