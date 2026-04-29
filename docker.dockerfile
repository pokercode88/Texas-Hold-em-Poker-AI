# Multi-stage build for Texas Hold'em AI System
FROM ubuntu:22.04 AS builder

# 避免交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装构建依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    python3 \
    python3-pip \
    python3-dev \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制源代码
COPY . .

# 构建C++部分
RUN mkdir -p build && cd build && \
    cmake .. && \
    make -j$(nproc)

# 安装Python依赖
RUN pip3 install --no-cache-dir -r requirements.txt

# 最终镜像
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libboost-system1.74.0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 从builder复制
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages

# 设置入口点
ENTRYPOINT ["python3", "examples/simple_game.py"]

# 默认命令
CMD ["--help"]