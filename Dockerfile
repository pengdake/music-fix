FROM docker.m.daocloud.io/python:3.10.12

EXPOSE 8000

# 避免交互
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
# 编译安装 chromaprint
COPY fpcalc /usr/local/bin/fpcalc

RUN chmod +x /usr/local/bin/fpcalc

RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建工作目录
WORKDIR /app

# 复制依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码

# 默认扫描目录
ENV MUSIC_DIR=/music
ENV ACOUSTID_API_KEY="Rz2fUjCuDH"

# 开发容器默认命令
CMD ["fastapi", "run", "main/app.py", "--host", "0.0.0.0", "--port", "8000"]

