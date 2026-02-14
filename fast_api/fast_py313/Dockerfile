# 使用更安全的 Python 版本作为基础镜像
FROM python:3.13

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器
COPY . /app

# 安装项目依赖（假设你有 requirements.txt）
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口（FastAPI 默认端口为 8000）
EXPOSE 8000

# 运行 FastAPI 应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

