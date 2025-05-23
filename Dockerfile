# --- 构建阶段 ---
FROM ubuntu:22.04 AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv build-essential cmake ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN cd /app/lib/silk && \
    make && make encoder && make decoder && \
    mv encoder decoder converter.sh /app/

# --- 运行阶段 ---
FROM python:3.11-slim AS final

ENV PORT=3000
WORKDIR /app

# 安装依赖
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# 创建并激活虚拟环境
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 仅复制必要文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝运行文件
COPY main.py .  
COPY api/ ./api/
COPY src/ ./src/
COPY --from=builder /app/encoder /app/decoder /app/converter.sh /app/

# 使用 JSON 格式 CMD，支持动态端口
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
