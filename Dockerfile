# 1️⃣ 베이스 스테이지
FROM python:3.11-slim AS base

# 환경 설정은 캐시 무효화가 거의 없음
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 2️⃣ OS 패키지 설치 (자주 안 바뀜)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# 3️⃣ requirements.txt만 먼저 복사 → pip install 레이어 캐시 분리
COPY requirements.txt ./

# pip 캐시 마운트 (BuildKit 필요)
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ 앱 소스 복사는 가장 마지막
COPY . .

# 5️⃣ 런타임 스테이지
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 6️⃣ 필요한 파일만 복사
COPY --from=base /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=base /app /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]