#!/bin/bash

# 设置工作目录
cd "$(dirname "$0")"

# 检查并停止已运行的Flask进程
echo "检查并停止已运行的Flask进程..."
pkill -f "python app.py"

# 检查venv目录是否存在
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "安装依赖..."
    pip install flask onnxruntime-web pillow
else
    source venv/bin/activate
fi

# 清理指定端口的进程
clean_port() {
    local port=$1
    local pids=$(lsof -t -i :$port)
    if [ ! -z "$pids" ]; then
        echo "发现端口 $port 被占用，正在清理进程..."
        echo $pids | xargs kill -9
        echo "端口 $port 已清理完成"
    fi
}

# 设置并清理端口
PORT=5000
clean_port $PORT

# 启动Flask应用
echo "启动应用程序在端口 $PORT..."
FLASK_RUN_PORT=$PORT python app.py